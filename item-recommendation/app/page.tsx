'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';
import useRainbow from './rainbow';

const analyzeImageForTextColor = async (imgElement: HTMLImageElement): Promise<boolean> => {
  return new Promise((resolve, reject) => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    if (!context) {
      reject(new Error('Could not get canvas context'));
      return;
    }

    if (!imgElement.complete) {
      imgElement.onload = () => processImage(imgElement, canvas, context, resolve);
      imgElement.onerror = () => reject(new Error('Image failed to load'));
    } else {
      processImage(imgElement, canvas, context, resolve);
    }
  });
};

const processImage = (
  imgElement: HTMLImageElement,
  canvas: HTMLCanvasElement,
  context: CanvasRenderingContext2D,
  resolve: (useWhiteText: boolean) => void
) => {
  canvas.width = imgElement.width;
  canvas.height = imgElement.height;

  context.drawImage(imgElement, 0, 0, imgElement.width, imgElement.height);
  const imageData = context.getImageData(0, 0, imgElement.width, imgElement.height);
  const { data } = imageData;

  let totalLuminance = 0;
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];
    const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    totalLuminance += luminance;
  }

  const avgLuminance = totalLuminance / (imgElement.width * imgElement.height);
  resolve(avgLuminance <= 128);
};

const Home = () => {
  const colors = useRainbow({intervalDelay: 250});
  const colorKeys = Object.keys(colors);
  const transitionDelay = 250 * 1.25;
  const rainbowStyleObject = {
    ...colors,
    transition: `
      ${colorKeys[0]} ${transitionDelay}ms linear,
      ${colorKeys[1]} ${transitionDelay}ms linear,
      ${colorKeys[2]} ${transitionDelay}ms linear
    `,
    background: `
      radial-gradient(
        circle at top left,
        var(${colorKeys[2]}),
        var(${colorKeys[1]}),
        var(${colorKeys[0]})
      )
    `
  };
  
  interface Item {
    id: string;
    name: string;
    description: string;
    price: number;
    image_url: string;
    buy_link?: string;
  }
  interface HistoryItem {
    id: string;
    name: string;
    description: string;
    price: number;
    image_url: string;
    buy_link?: string;
    liked: boolean;
  }
  const [item, setItem] = useState<Item | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [preference, setPreference] = useState<number[]>(new Array(4096).fill(0));
  const [alreadySeen, setAlreadySeen] = useState<HistoryItem[]>([]);
  const [whiteText, setWhiteText] = useState<boolean>(false);
  const mainUrl = 'http://127.0.0.1:5000/';
  const fetchItem = async () => {
    setLoading(true);
    try {
      const response = await axios.get<Item>(mainUrl);
      setItem(response.data);
    } catch (error) {
      console.error('Error fetching dress:', error);
    } finally {
      setLoading(false);
    }
  };
  const handlePreferenceUpdate = async (like: boolean) => {
    if (!item) {
      console.error('No item to act on');
      return;
    }
    try {
      const response = await axios.post(mainUrl, {
        like,
        preference,
        already_seen: [...alreadySeen.map((x) => x.id), item.id],
        item_id: item.id, // Send the current item's ID
      });
      setAlreadySeen((prev) => [...prev, {...item, liked: like}]);
      setPreference(response.data.preference);
      setItem({
        id: response.data.id,
        buy_link: response.data.buy_link,
        name: response.data.name,
        description: response.data.description,
        price: response.data.price,
        image_url: response.data.image_url,
      });
    } catch (error) {
      console.error('Error updating preferences:', error);
    }
  };
  useEffect(() => {
    if (!item?.image_url) return;
    const proxyImageUrl = `${mainUrl}/proxy-image?url=https://www.na-kd.com${item.image_url}`;
    const img = new Image();
    img.crossOrigin = 'anonymous'; // Enable CORS for the proxied image
    img.src = proxyImageUrl;
    analyzeImageForTextColor(img)
      .then((useWhiteText) => {
        setWhiteText(useWhiteText);
      })
      .catch((error) => console.error('Error analyzing image:', error));
  }, [item]);
  useEffect(() => {
    fetchItem();
  }, []);
  if (loading) return <div>Loading...</div>;
  if (!item)
    return <div>No dresses available. Please try refreshing the page later.</div>;
  return <>
    <div className='h-40 text-black mb-8'>
      <div className="flex items-center overflow-x-auto whitespace-nowrap w-full max-w-none pt-2 pl-2 pr-2 pb-1">
        {alreadySeen.map((item) => {
          return <a className='relative flex bg-cover cursor-pointer mr-2 min-w-[96px]'
            key={item.id}
            href={`https://na-kd.com${item.buy_link}`}
            target='_blank'>
            <img src={`https://na-kd.com${item.image_url}`}
                className='mt-2 h-28 w-24 object-cover border-2 border-black' alt='item'/>
            <div className={`absolute top-0 -right-3 p-1 rounded-full border-2 border-black ${item.liked ? 'bg-green': 'bg-red'}`}>
              <Svg className='w-5 h-5 bg-black' src={item.liked ? '/heart.svg' : '/heart-crack.svg'}/>
            </div>
          </a>
        })}
      </div>
    </div>
    <div className='w-full flex-col flex items-center'>
      <div className='flex flex-col item-center w-96'>
        <div className='relative h-[560px] mb-4'>
          <img className='w-96 h-[560px] inset-0 translate-x-1.5 translate-y-1.5 object-cover'
              src={`https://www.na-kd.com${item.image_url}`} alt='item'/>
          <h2 className={`w-full absolute bottom-4 text-lg ${whiteText?'text-white':'text-black'} text-center absolute-x-center lexend`}>
            {item.name}
          </h2>
          <div className='absolute top-0 left-0 bottom-0 right-0 border-2 border-black'/>
        </div>
        <div className='flex flex-col'>
          <div className='flex grid-cols-2 gap-4 mb-4'>
            <button className='h-12 w-full group relative focus:outline-none' 
                onClick={() => handlePreferenceUpdate(false)}>
              <span className='absolute inset-0 translate-x-1.5 translate-y-1.5 bg-red'/>
              <span
                className='absolute top-0 left-0 bottom-0 right-0 border-2 border-black text-black font-bold
                    group-hover:translate-x-1.5 group-hover:translate-y-1.5 transition-transform flex items-center justify-center'>
                <Svg src='/heart-crack.svg' className='w-5 h-5 mr-2 bg-black'/>
                모든
              </span>
            </button>
            <button className='h-12 w-full group relative focus:outline-none'
                onClick={() => handlePreferenceUpdate(true)}>
              <span className='absolute inset-0 translate-x-1.5 translate-y-1.5 bg-green'/>
              <span
                className='absolute top-0 left-0 bottom-0 right-0 border-2 border-black text-black font-bold
                    group-hover:translate-x-1.5 group-hover:translate-y-1.5 transition-transform flex items-center justify-center'>
                <Svg src='/heart.svg' className='w-5 h-5 mr-2 bg-black'/>
                인류
              </span>
            </button>
          </div>
          <div>
            <a
              href={'https://www.na-kd.com' + item.buy_link || '#'}
              target="_blank"
              rel="noopener noreferrer"
            >
              <button className='h-12 w-full group relative inline-block focus:outline-none'>
                <span className='absolute inset-0 translate-x-1.5 translate-y-1.5' style={rainbowStyleObject}/>
                <span
                  className='absolute top-0 left-0 bottom-0 right-0 border-2 border-black text-black font-bold
                      group-hover:translate-x-1.5 group-hover:translate-y-1.5 transition-transform flex items-center justify-center'>
                  <Svg src='/cart-shopping.svg' className='w-5 h-5 mr-2 bg-black'/>
                  구성원의
                </span>
              </button>
            </a>
          </div>
        </div>
      </div>
    </div>
  </>;
};

function Svg(
  { 
		src,
    className='',
  }: {
		src: string,
    className?: string,
  }
) {
  return <div className={`${className}`} style={{
		maskSize: '100%',
		maskRepeat: 'no-repeat',
		maskPosition: 'center',
		WebkitMaskRepeat: 'no-repeat',
		maskImage: `url(${src})`,
		WebkitMaskImage: `url(${src})`,
	}}/>
}

export default Home;
