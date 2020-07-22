import React, { Component } from 'react';
import { Input, Button, Divider, Descriptions, message } from 'antd'
import { CheckOutlined } from '@ant-design/icons'
import axios from 'axios'

export class Start1 extends Component {
    constructor() {
        super()
        this.state = {
            ques_type : '',
            upload_time : '',
            code_similarity : '',
            code_time_complexity : '',
            code_space_complexity : '',
            overall_access : '',
        }
    }

    get_report() {
        let student_id = document.getElementById("student-id")
        let ques_id = document.getElementById("ques-id")
        let student_id_val = String(student_id.value)
        let ques_id_val = String(ques_id.value)
        // console.log('student: ' + student_id_val + ' ' +'ques: ' + ques_id_val)
        axios.get(`http://localhost:5000/report/student_id=${student_id_val}/ques_id=${ques_id_val}`)
        .then(response => {
            let data = response.data
            console.log(data)
            if(data.message === "Invalid Input") {
                message.warning("学生id和题目id不可为空!")
            }else if(data.message === "Valid Input") {
                this.setState({
                    ques_type : data.ques_type,
                    upload_time : data.upload_time,
                    code_similarity : data.code_similarity,
                    code_time_complexity : data.code_time_complexity,
                    code_space_complexity : data.code_space_complexity,
                    overall_access : data.overall_access,
                })
            }
        })
        .catch(error => {
            console.log(error)
        })
    }

    render() {
        return (
            <div className="startlayout">
                <Input placeholder="请输入学生 id :" id="student-id"></Input>
                <Divider type="vertical"/>
                <Input placeholder="请输入题目 id :" id="ques-id"></Input>
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
                    <Descriptions.Item label="整体评价">
                        { this.state.overall_access }
                    </Descriptions.Item>
                </Descriptions>
            </div>
        )
    }
}

export default Start1;
