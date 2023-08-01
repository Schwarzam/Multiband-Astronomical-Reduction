import React, { useState } from 'react';

const ArrowButton = ({children}) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const handleClick = () => {
    setIsOpen(!isOpen);
  }

  return (
    <>
      <button className="fixed bottom-2 right-1 flex transform -translate-x-1/2 z-50" onClick={handleClick}>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={`h-6 w-6 transform ${isOpen ? 'rotate-180' : ''}`} >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
        <spam>Logs</spam>
      </button>
      
      {isOpen && (
        <div className="fixed bottom-0 left-0 h-1/2 w-screen bg-gray-100 overflow-auto transition-height duration-500 ease-in-out z-40 outline">
          <div className="p-6">
            {children}
          </div>
        </div>
      )}
    </>
  );
}

export default ArrowButton;
