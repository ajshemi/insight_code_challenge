// import logo from './logo.svg';
import './App.css';
import Chart from "react-google-charts";

function App() {



 
  return (
    <div className="App">
      {/* <header className="App-header"> */}

      <Chart
  chartType="BarChart"
  spreadSheetUrl="https://docs.google.com/spreadsheets/d/1VQRy0fArI12OMZ7EXew4cOC_t70j3IxYCSwp0igPZvg/edit#gid=0"
  options={{
    hAxis: {
      format: 'short',
    },
    vAxis: {
      format: 'decimal',
      // format:'scientific'
      // format:'long'
      // format:'percent'
    },
  }}
  rootProps={{ 'data-testid': '1' }}
/>
   {/* <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a> */}
      {/* </header> */}
    </div>
  );
}

export default App;
