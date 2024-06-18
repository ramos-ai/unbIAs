import { useState } from "react";
import { useEffect } from "react";
import copyImg from "../assets/copy.svg";

const TranslationGender = ({ translations, optionNeutral }) => {
  const [titles, setTitles] = useState([]);
  const [data, setData] = useState({});

  useEffect(() => {
    if (translations) {
      setData(translations);
    }
  }, [translations]);

  const formatNeutral = (translation) => {
    if (translation) {
      return translation.replaceAll("[x]", optionNeutral["label"]);
    }
    return "";
  };

  useEffect(() => {
    if (data) {
      getLabels();
    }
  }, [data]);

  const getLabels = () => {
    let labels = [];

    Object.keys(translations).forEach((key) => {
      if (key === "first_option") {
        labels.push("Primeira opção: ");
      } else if (key === "second_option") {
        labels.push("Segunda opção: ");
      } else if (key === "neutral") {
        labels.push("Neutro: ");
      } else if (key === "translation") {
        labels.push("Tradução: ");
      } else if (key === "more_likely") {
        labels.push("Mais provável: ");
      } else if (key === "less_likely") {
        labels.push("Menos provável: ");
      }

      setTitles(labels);
    });
  };

  function copyRoomCodeToClipboard(translation) {
    navigator.clipboard.writeText(translation);
  }

  return (
    <div className='traducao'>
      <div className='title'>Traduções:</div>
      {data &&
        Object.values(data)?.map((translation, index) => {
          return (
            <>
              <div className='textarea-container'>
                <div className='title-gender'>{titles[index]}</div>
                <textarea
                  className='translations-textarea'
                  disabled
                  value={formatNeutral(translation)}></textarea>
                <button
                  className='botao-copiar'
                  onClick={() => copyRoomCodeToClipboard(translation)}>
                  <img className='img-copiar' src={copyImg} alt='Copiar' />
                </button>
              </div>
            </>
          );
        })}
    </div>
  );
};

export default TranslationGender;
