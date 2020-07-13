import React, { Component } from 'react';
import 'antd/dist/antd.css'
import { Input, Button, Divider, Descriptions } from 'antd'
import { CheckOutlined } from '@ant-design/icons'

export class Start extends Component {
    constructor() {
        super()
        this.state = {
            ques_type : '',
            upload_time : '',
            code_similarity : '',
            code_time_complexity : '',
            code_space_complexity : '',
            overall_access : ''
        }
    }

    get_report() {
        console.log(this.state)
        fetch("http://localhost:5000/report").then(response => 
            response.json().then(data => {
                console.log(data)
                this.setState({
                    ques_type : data.ques_type,
                    upload_time : data.upload_time,
                    code_similarity : data.code_similarity,
                    code_time_complexity : data.code_time_complexity,
                    code_space_complexity : data.code_space_complexity,
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
                <Descriptions title="学生编程评价报告" bordered className="description-text">
                    <Descriptions.Item label="题目分组">
                        { this.state.ques_type }
                    </Descriptions.Item>
                    <Descriptions.Item label="最后提交时间">
                        { this.state.upload_time }
                    </Descriptions.Item>
                    <Descriptions.Item label="代码相似度">
                        { this.state.code_similarity } %
                    </Descriptions.Item>
                    <Descriptions.Item label="代码时间复杂度">
                        { this.state.code_time_complexity }
                    </Descriptions.Item>
                    <Descriptions.Item label="代码空间复杂度">
                        { this.state.code_space_complexity }
                    </Descriptions.Item>
                    <Descriptions.Item label="整体评价" span={4}>
                        { this.state.overall_access }
                    </Descriptions.Item>
                </Descriptions>
            </div>
        )
    }
}

export default Start;
