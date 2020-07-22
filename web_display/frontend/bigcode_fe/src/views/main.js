import React, { Component } from 'react'
import 'antd/dist/antd.css'
import { Start1 } from '../components/Start1'
import { Start2 } from '../components/Start2'
import { Guide } from '../components/Guide'
import { Tabs } from 'antd'
import { CopyrightCircleOutlined } from '@ant-design/icons'

const { TabPane } = Tabs

export class main extends Component {
    render() {
        return (
            <div className="layout">
                <div className="header">
                    <span className="header-text">Code Evaluation Tool</span>
                </div>
                <div className="main">
                    <Tabs defaultActiveKey="1" size="large">
                        <TabPane tab="工具介绍" key="1">
                            <Guide />
                        </TabPane>
                        <TabPane tab="单题代码质量" key="2">
                            <Start1 />
                        </TabPane>
                        <TabPane tab="综合代码质量" key="3">
                            <Start2 />
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
