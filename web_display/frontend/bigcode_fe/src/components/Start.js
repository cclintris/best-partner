import React, { Component } from 'react';
import { Input } from 'antd'

export class Start extends Component {
    render() {
        return (
            <div className="startlayout">
                <Input placeholder="请输入学生 id :" id="inputStudentid"></Input>
            </div>
        )
    }
}

export default Start;
