import React, { Component } from 'react'
import { Input, Button, Divider, message } from 'antd'
import { CheckOutlined } from '@ant-design/icons'
import { Echart } from '../components/Echart'
import axios from 'axios'

export class Start2 extends Component {
    constructor() {
        super()
        this.state = {
            overall_student_value : [],
            specific_student_value : [],
        }
    }

    get_overall_report(){
        let student_id = document.getElementById("student-id1")
        let student_id_val = String(student_id.value)
        axios.get(`http://localhost:5000/Echartreport/student_id=${student_id_val}`)
        .then(response => {
            let data = response.data
            console.log(data)
            if(data.message === "Invalid Input") {
                message.warning("学生id不可为空!")
            }else if(data.message === "Valid Input") {
                this.setState({
                    overall_student_value : data.overall_student_value,
                    specific_student_value : data.specific_student_value,
                })
                // console.log(this.state.overall_student_value)
                // console.log(this.state.specific_student_value)
            }
        })
        .catch(error => {
            console.log(error)
        })
    }

    render () {
        return (
            <div className="startlayout"> 
                <Input placeholder="请输入学生 id :" id="student-id1"></Input>
                <Divider type="vertical"/>
                <Button type="primary" 
                        icon={<CheckOutlined />} 
                        onClick={() => this.get_overall_report()}>
                        确认
                </Button>
                <Echart 
                    overall_student_value = { this.state.overall_student_value } 
                    specific_student_value = { this.state.specific_student_value }
                />
            </div>
        )
    }
}

export default Start2
