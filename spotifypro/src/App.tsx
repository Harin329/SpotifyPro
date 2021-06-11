import { FC } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Home from "./pages/home";

const App: FC = () => (
  <Router>
    <Route exact path="/" component={Home} />
  </Router>
);

export default App;
