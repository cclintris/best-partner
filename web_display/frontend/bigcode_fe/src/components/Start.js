import React, { Component } from 'react';
import 'antd/dist/antd.css'
import { Input } from 'antd'
import { Button } from 'antd'
import { Divider } from 'antd'
import { CheckOutlined } from '@ant-design/icons'
import { Descriptions } from 'antd'

export class Start extends Component {
    constructor() {
        super()
        this.state = {
            student_name : '',
            student_id : '',
            code_similarity : '',
            code_complexity : '',
            overall_access : ''
        }
    }

    get_report() {
        console.log(this.state)
        fetch("http://localhost:5000/report").then(response => 
            response.json().then(data => {
                console.log(data)
                this.setState({
                    student_name : data.student_name,
                    student_id : data.student_id,
                    code_similarity : data.code_similarity,
                    code_complexity : data.code_complexity,
                    overall_access : data.overall_access
                })
            })
        )
    }

    render() {
        return (
            <div className="startlayout">
                <Input placeholder="请输入学生 id :" id="inputid"></Input>
                <Divider type="vertical"/>
                <Input placeholder="请输入题目 id :" id="inputid"></Input>
                <Divider type="vertical"/>
                <Button type="primary" 
                        icon={<CheckOutlined />} 
                        onClick={() => this.get_report()}>
                        确认
                </Button>
                <Divider />
                <Descriptions title="学生编程评价报告" bordered>
                    <Descriptions.Item label="学生姓名" span={1}>
                        { this.state.student_name }
                    </Descriptions.Item>
                    <Descriptions.Item label="学生学号" span={1}>
                        { this.state.student_id }
                    </Descriptions.Item>
                    <Descriptions.Item label="代码相似度" span={1}>
                        { this.state.code_similarity }%
                    </Descriptions.Item>
                    <Descriptions.Item label="代码时空复杂度" span={1}>
                        { this.state.code_complexity }
                    </Descriptions.Item>
                    <Descriptions.Item label="整体评价">
                        { this.state.overall_access }
                    </Descriptions.Item>
                </Descriptions>
            </div>
        )
    }
}

export default Start;
