import './App.css';
import ChatBotWidget from "./components/ChatBotWidget"
import "./components/styles/chatbot.css"
import poster from "./assests/geely-poster.png"

function App() {
  return (
    <div className='main-content' >
      <img src={poster} className='main-img' alt="Geely Poster" />
      <ChatBotWidget />
    </div>
  );
}

export default App;
