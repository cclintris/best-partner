import React, { Component } from 'react'
import { Collapse } from 'antd'
import { QuestionCircleOutlined, TeamOutlined, ToolOutlined, GithubOutlined } from '@ant-design/icons'

const { Panel } = Collapse

const addIconPanel1 = () => (
    <QuestionCircleOutlined />
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
                        <p>本产品是一款用于分析和检验学生python编程代码质量的工具。该工具使用后台的文本处理程序对每个学生完成的代码样本进行分析和校验，并利用统计工具得出恰当的学生总体水平，用以和学生个体的能力做出对比和评价，并将对比的结果以表格和雷达图的形式向用户展示出来。
                        本产品目前仍处于测试阶段，功能使用当中会产生一定的偏差，如发现异常欢迎与开发者进行联系和沟通。
                        </p>
                    </Panel>
                    <Panel 
                        key='2' 
                        header='服务对象以及适用群体' 
                        extra={ addIconPanel2() }>
                        <p>
                        本产品的服务对象为一般的编程初学者、学生以及相关专业教师。本产品的适用群体具有以下特点中的一项或多项：<br />
                        1. 用户具有一定的python编程基础<br />
                        2. 用户进行过一定题量的python算法练习<br />
                        3. 用户处在需要评估代码质量的小规模的工作集群（如学生班级、工作小组）中或需要对该种工作集群中的人员进行评估<br />
                        4. 用户练习时使用小规模的练习题库
                        </p>
                    </Panel>
                    <Panel 
                        key='3' 
                        header='使用教学' 
                        extra={ addIconPanel3() }>
                        <p>
                        本产品的使用流程如下：<br />
                        1. 上传代码url的json配置文件(或使用系统的预置文件)<br />
                        2. 在初始化界面进行分析库初始化<br />
                        3. 等待一定时间，返回网页<br />
                        4. 键入人员的id和题目id查询单题评价<br />
                        5. 键入人员id查询人员评价
                        </p>
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
