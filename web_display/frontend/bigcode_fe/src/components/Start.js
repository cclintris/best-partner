import React, { Component } from 'react';
import 'antd/dist/antd.css'
import { Input } from 'antd'
import { Button } from 'antd'
import { Divider } from 'antd'
import { CheckOutlined } from '@ant-design/icons'
import { Descriptions } from 'antd'

export class Start extends Component {
    state = {
        report_status : {
            student_name : '林希澄',
            student_id : '181250083',
            code_similarity : 25,
            code_complexity : 'O(n)',
            overall_access : '菜鸡一个'
        }
    }

    report_status_ref = this.state.report_status

    confirm = () => {
        console.log("confirm student id")
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
                        onClick={() => this.confirm()}>
                        确认
                </Button>
                <Divider />
                <Descriptions title="学生编程评价报告" bordered>
                    <Descriptions.Item label="学生姓名" span={1}>
                        { this.report_status_ref.student_name }
                    </Descriptions.Item>
                    <Descriptions.Item label="学生学号" span={1}>
                        { this.report_status_ref.student_id }
                    </Descriptions.Item>
                    <Descriptions.Item label="代码相似度" span={1}>
                        { this.report_status_ref.code_similarity }%
                    </Descriptions.Item>
                    <Descriptions.Item label="代码时空复杂度" span={1}>
                        { this.report_status_ref.code_complexity }
                    </Descriptions.Item>
                    <Descriptions.Item label="整体评价">
                        { this.report_status_ref.overall_access }
                    </Descriptions.Item>
                </Descriptions>
            </div>
        )
    }
}

export default Start;
