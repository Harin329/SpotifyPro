import React, { FC } from "react";
import { Layout, Row, Col } from "antd";
import "./index.css";
const { Header, Content } = Layout;

const Room: FC = () => (
  <Row className="App">
    <Col className="App-sider" span={6}>
      col-12
    </Col>
    <Col span={12}>col-12</Col>
  </Row>
);

export default Room;
