import { useEffect } from "react";
import copyImg from "../assets/copy.svg";

const PossibleWords = ({ translations, optionNeutral }) => {
  const titles = ["Masculino: ", "Feminino: ", "Neutro: "];

  const formatNeutral = (translation) => {
    if (translation) {
      return translation.replaceAll("[x]", optionNeutral["label"]);
    }
    return "";
  };

  function copyRoomCodeToClipboard(translation) {
    navigator.clipboard.writeText(translation);
  }

  return (
    <div className='traducao'>
      <div className='title'>Possíveis traduções:</div>
      {translations &&
        translations["possible_words"]?.map((translation, index) => {
          return (
            <>
              <div className='textarea-container' key={index}>
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

export default PossibleWords;
