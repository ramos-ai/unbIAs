import error from "../assets/error-red.png";

export function Error() {
  return (
    <div className='error-pg'>
      <div>
        <img className='img-error' src={error} alt='error' />
      </div>
      <div className='error-msg'>
        <div className='ops-text'>...oooops</div>
        <div className='sub-error'>
          <span>Tente novamente.</span>
        </div>
      </div>
    </div>
  );
}
