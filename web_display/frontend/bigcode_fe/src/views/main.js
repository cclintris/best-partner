import React, { Component } from 'react';
import 'antd/dist/antd.css';
import { Start } from '../components/Start';
import { Tabs } from 'antd';

const { TabPane } = Tabs;

export class main extends Component {
    render() {
        return (
            <div className="layout">
                <div className="header">
                    BigCode Tool
                </div>
                <div className="main">
                    <Tabs defaultActiveKey="1" size="large">
                        <TabPane tab="工具介绍" key="1">
                            Content of Tab Pane 1
                        </TabPane>
                        <TabPane tab="开始使用" key="2">
                            <Start />
                        </TabPane>
                    </Tabs>
                </div>
                <div className="footer">

                </div>
            </div>
        )
    }
}

export default main
