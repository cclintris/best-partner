import React, { Component } from 'react'
import { Input, Button, Divider } from 'antd'
import { CheckOutlined } from '@ant-design/icons'
import { Echart } from '../components/Echart'

export class Start2 extends Component {
    get_overall_report = () => {
        console.log("overall report")
    }

    render () {
        return (
            <div className="startlayout"> 
                <Input placeholder="请输入学生 id :" id="student-id"></Input>
                <Divider type="vertical"/>
                <Button type="primary" 
                        icon={<CheckOutlined />} 
                        onClick={() => this.get_overall_report()}>
                        确认
                </Button>
                <Echart />
            </div>
        )
    }
}

export default Start2
