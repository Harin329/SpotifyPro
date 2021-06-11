import { FC } from "react";
import { Typography, Row, Button } from "antd";
import "./index.css";

const { Title } = Typography;

const authorizeSpotify = () => {
  console.log("Authorizing Spotify");
}

const Home: FC = () => (
  <Row className="App">
    <div style={{ flexDirection: "row" }}>
      <Title style={{color: 'white'}}>Welcome to SoundTown!</Title>
      <Button type="primary" shape="round" size="large" onClick={authorizeSpotify}>
        Authorize with Spotify
      </Button>
    </div>
  </Row>
);

export default Home;
