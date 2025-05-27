import { useRef } from 'react'
import './App.css'
import { processAnalysis } from './process'

export const BASE_URL = import.meta.env.VITE_BASE_URL

function App() {
  const commendRef = useRef()
  const suggestRef = useRef()

  // const handleSubmit = async(type) => {
  //   console.log(type)
  //   try {
  //     const response = await fetch(BASE_URL+'/api/gather', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ type: type }),
  //     });

  //     if (!response.ok) {
  //       throw new Error(`HTTP error! status: ${response.status}`);
  //     }

  //     const data = await response.json();
  //     const botResponse = await processAnalysis(data.text,type)

  //     if(type == 'Commented'){
  //       commendRef.current.value=botResponse
  //     } else{
  //       suggestRef.current.value=botResponse
  //     }
  //   } catch (err) {
  //     console.log(err);
  //   }
  // }

  const handleSubmit = async(type) => {
    try {
      const response = await fetch(BASE_URL+'/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type: type }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} error: ${response.error}`);
      }

      const data = await response.json();
      if(type == 'Commended'){
        commendRef.current.value=data.analysis
      } else{
        suggestRef.current.value=data.analysis
      }
    } catch (err) {
      console.log(err);
    }
  }

  return (
    <div className='main'>
      <div className='container'>
          <div className="form-group">
            <button type="button" onClick={() => handleSubmit('Commended')}>Most praised features?</button>
            <textarea
              id="commended"
              name="commended"
              rows="6"
              ref={commendRef}
              placeholder="Most Commended features/product..."
            ></textarea>
          </div>
          <div className="form-group">
            <button type="button" onClick={() => handleSubmit('Suggested')}>Most demanded features?</button>
            <textarea
              id="suggested"
              name="suggested"
              rows="6"
              ref={suggestRef}
              placeholder="Suggested features/products..."
            ></textarea>
          </div>
      </div>
      <iframe
        src= {BASE_URL+"/dashboard"} // URL where Dash app is routed
        title="Dash Plot"
      ></iframe>
    </div>
  )
}

export default App
