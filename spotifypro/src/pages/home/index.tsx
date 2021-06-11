import React, { FC } from "react";
import { Layout, Row, Col } from "antd";
import "./index.css";
const { Header, Content } = Layout;

const Home: FC = () => (
  <Layout className="App">
    <Header className="App-header">Spotify Pro</Header>
    <Layout>
      <Content className="App-sider">
        <Row className="App-sider">
          <Col className="App-sider" span={6}>col-12</Col>
          <Col span={12}>col-12</Col>
        </Row>
      </Content>
    </Layout>
  </Layout>
);

export default Home;
