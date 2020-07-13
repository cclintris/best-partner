import React, { Component } from 'react'
import { Collapse } from 'antd'
import { QuestionCircleOutlined, TeamOutlined, ToolOutlined, GithubOutlined } from '@ant-design/icons'

const { Panel } = Collapse

const addIconPanel1 = () => (
    <QuestionCircleOutlined/>
);

const addIconPanel2 = () => (
    <TeamOutlined />
);

const addIconPanel3 = () => (
    <ToolOutlined />
);

const addIconPanel4 = () => (
    <GithubOutlined />
);

const textPanel1 = ``

const textPanel2 = ``

const textPanel3 = ``

const textPanel4 = `
    GitHub 地址 :
`

export class Guide extends Component {
    render() {
        return (
            <div>
                <Collapse defaultActivekey={['1']}>
                    <Panel 
                        key='1' 
                        header='关于 Code Evaluation Tool' 
                        extra={ addIconPanel1() }>
                    </Panel>
                    <Panel 
                        key='2' 
                        header='服务对象以及适用群体' 
                        extra={ addIconPanel2() }>
                    </Panel>
                    <Panel 
                        key='3' 
                        header='使用教学' 
                        extra={ addIconPanel3() }>
                    </Panel>
                    <Panel 
                        key='4' 
                        header='GitHub 开源项目' 
                        extra={ addIconPanel4() }>
                        { textPanel4 } 
                        <a href="https://github.com/cclintris/BigCode">https://github.com/cclintris/BigCode</a>
                    </Panel>
                </Collapse>
            </div>
        )
    }
}

export default Guide
