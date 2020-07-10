import React, { Component } from 'react'
import 'antd/dist/antd.css'
import { Start } from '../components/Start'
import { Tabs } from 'antd'
import { DingtalkOutlined } from '@ant-design/icons'
import { CopyrightCircleOutlined } from '@ant-design/icons'

const { TabPane } = Tabs

export class main extends Component {
    render() {
        return (
            <div className="layout">
                <div className="header">
                    <DingtalkOutlined></DingtalkOutlined>
                    <span className="header-text">Code Evaluation Tool</span>
                </div>
                <div className="main">
                    <Tabs defaultActiveKey="1" size="large">
                        <TabPane tab="工具介绍" key="1">
                            README of tool usage
                        </TabPane>
                        <TabPane tab="开始使用" key="2">
                            <Start />
                        </TabPane>
                    </Tabs>
                </div>
                <div className="footer">
                    <span className="footer-text">
                        数据科学基础大作业 / 由 BigCode 小组开发
                        <CopyrightCircleOutlined />
                    </span>
                </div>
            </div>
        )
    }
}

export default main
