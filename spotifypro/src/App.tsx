import { FC } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Home from "./pages/home";

const App: FC = () => (
  <Router>
    <Route exact path="/" component={Home} />
    <Route exact path="/createRoom" component={Home} />
    <Route exact path="/room/:id" component={Home} />
  </Router>
);

export default App;
