import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import SciByFilter from "../Calendar/sciByFilter";
import SciBlock from "../Calendar/sci";
import FlatByFilter from "../Calendar/flatByFilter";
import FlatBlock from "../Calendar/flat";
import BiasBlock from "../Calendar/biasBlock";
import FinalBlock from "../Calendar/finalTiles";

import React from 'react';

import { PanZoom } from 'react-easy-panzoom'

import { useState } from "react";

export default class Display {
    constructor(type) {
        this.type = type
        this.panZoomRef = React.createRef();

        this.sum = 0;
        this.checkboxes = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512];
        this.sumElement = null;
    }


    statos = null
    statos2 = null
    comment = null

    targetId = null
    code = ''

    fragments = []
    tabs = []
    tabsContent = []
    aditionals = []

    addFragments = (item, value) => {
        if (value !== null) {
            if (value.toString().includes('.png')) {
                this.tabs.push(item)
                this.tabsContent.push(value)
                return
            }
        }
        if (value !== null) {
            this.fragments.push({ item: item, value: value })
        }

    }

    addAditionals = (item) => {
        this.aditionals.push(item)
    }

    process = () => {
        if (this.type === 'fin') {
            const t = new FinalBlock()
            t.processObjectById(this.fragments[0].value, this.code)
        }
        if (this.type === 'scif') {
            const t = new SciByFilter()
            t.processObjectById(this.fragments[0].value, this.code)
        }
        if (this.type === 'sci') {
            const t = new SciBlock()
            t.processObjectById(this.fragments[0].value, this.code)
        }
        if (this.type === 'flatf') {
            const t = new FlatByFilter()
            t.processObjectById(this.fragments[0].value, this.code)
        }
        if (this.type === 'flat') {
            const t = new FlatBlock()
            t.processObjectById(this.fragments[0].value, this.code)
        }
        if (this.type === 'bias') {
            const t = new BiasBlock()
            t.processObjectById(this.fragments[0].value, this.code)
        }
    }

    setStatus = () => {
        if (this.type === 'fin') {
            const t = new FinalBlock()
            t.setStatus(this.fragments[0].value, this.statos)
        }
        if (this.type === 'scif') {
            const t = new SciByFilter()
            t.setStatus(this.fragments[0].value, this.statos)
        }
        if (this.type === 'sci') {
            const t = new SciBlock()
            t.setStatus(this.fragments[0].value, this.statos)
        }
        if (this.type === 'flatf') {
            const t = new FlatByFilter()
            t.setStatus(this.fragments[0].value, this.statos)
        }
        if (this.type === 'flat') {
            const t = new FlatBlock()
            t.setStatus(this.fragments[0].value, this.statos)
        }
        if (this.type === 'bias') {
            const t = new BiasBlock()
            t.setStatus(this.fragments[0].value, this.statos)
        }
    }

    setSubStatus = () => {
        if (this.type === 'fin') {
            const t = new FinalBlock()
            t.setSubStatus(this.fragments[0].value, this.statos2)
        }
        if (this.type === 'scif') {
            const t = new SciByFilter()
            t.setSubStatus(this.fragments[0].value, this.statos2)
        }
        if (this.type === 'sci') {
            const t = new SciBlock()
            t.setSubStatus(this.fragments[0].value, this.statos2)
        }
        if (this.type === 'flatf') {
            const t = new FlatByFilter()
            t.setSubStatus(this.fragments[0].value, this.statos2)
        }
        if (this.type === 'flat') {
            const t = new FlatBlock()
            t.setSubStatus(this.fragments[0].value, this.statos2)
        }
        if (this.type === 'bias') {
            const t = new BiasBlock()
            t.setSubStatus(this.fragments[0].value, this.statos2)
        }
    }

    validate = () => {
        if (this.type === 'scif') {
            const t = new SciByFilter()
            t.validate(this.fragments[0].value)
        }
        if (this.type === 'sci') {
            const t = new SciBlock()
            t.validate(this.fragments[0].value)
        }
        if (this.type === 'flatf') {
            const t = new FlatByFilter()
            t.validate(this.fragments[0].value)
        }
        if (this.type === 'flat') {
            const t = new FlatBlock()
            t.validate(this.fragments[0].value)
        }
        if (this.type === 'bias') {
            const t = new BiasBlock()
            t.validate(this.fragments[0].value)
        }
    }

    setComment = () => {
        if (this.type === 'fin') {
            const t = new FinalBlock()
            t.setComment(this.fragments[0].value, this.comment)
        }
        if (this.type === 'scif') {
            const t = new SciByFilter()
            t.setComment(this.fragments[0].value, this.comment)
        }
        if (this.type === 'sci') {
            const t = new SciBlock()
            t.setComment(this.fragments[0].value, this.comment)
        }
        if (this.type === 'flatf') {
            const t = new FlatByFilter()
            t.setComment(this.fragments[0].value, this.comment)
        }
        if (this.type === 'flat') {
            const t = new FlatBlock()
            t.setComment(this.fragments[0].value, this.comment)
        }
        if (this.type === 'bias') {
            const t = new BiasBlock()
            t.setComment(this.fragments[0].value, this.comment)
        }
    }

    add = () => {
        if (this.type === 'scif') {
            const t = new SciByFilter()
            t.add(this.fragments[0].value, this.targetId)
        }
        if (this.type === 'sci') {
            const t = new SciBlock()
            t.add(this.fragments[0].value, this.targetId)
        }
        if (this.type === 'flatf') {
            const t = new FlatByFilter()
            t.add(this.fragments[0].value, this.targetId)
        }
        if (this.type === 'flat') {
            const t = new FlatBlock()
            t.add(this.fragments[0].value, this.targetId)
        }
        if (this.type === 'bias') {
            const t = new BiasBlock()
            t.add(this.fragments[0].value, this.targetId)
        }
    }

    remove = () => {
        if (this.type === 'scif') {
            const t = new SciByFilter()
            t.remove(this.fragments[0].value, this.targetId)
        }
        if (this.type === 'sci') {
            const t = new SciBlock()
            t.remove(this.fragments[0].value, this.targetId)
        }
        if (this.type === 'flatf') {
            const t = new FlatByFilter()
            t.remove(this.fragments[0].value, this.targetId)
        }
        if (this.type === 'flat') {
            const t = new FlatBlock()
            t.remove(this.fragments[0].value, this.targetId)
        }
        if (this.type === 'bias') {
            const t = new BiasBlock()
            t.remove(this.fragments[0].value, this.targetId)
        }
    }

    setFlag = () => {
        if (this.type == 'fin') {
            const t = new FinalBlock()
            t.flag(this.fragments[0].value, this.sum)
        }
    }



    changeStatus(value) {
        this.statos = value
    }
    changeSubStatus(value) {
        this.statos2 = value
    }
    changeComment(value) {
        this.comment = value
    }
    changeCode(value) {
        this.code = value
    }
    changeTargetId(value) {
        this.targetId = value
    }

    handleCheck(value, event) {
        this.sum = event.target.checked ? this.sum + value : this.sum - value;
        document.getElementById(`${this.fragments[0].value}-sum`).innerHTML = `Sum ${this.sum}`;
    }


    handleStateChange = ({ scale }) => {
        if (scale < 1) {
            this.panZoomRef.current.reset();
        }
    };

    getFinal() {
        return (
            <div className='p-4'>
                {!(this.type === 'individual' || this.type === 'generical') && (
                    <div className="flex justify-center space-x-4 items-center mt-4">
                        <button
                            type="button"
                            onClick={() => { window.confirm("Process block " + this.fragments[0].value + "?") && this.process() }}
                            className="px-4 py-2 font-medium text-white bg-green-500 rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
                        >
                            Process
                        </button>

                        <input
                            className="px-3 py-2 w-72 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
                            onChange={(e) => this.changeCode(e.target.value)}
                            placeholder="execution code"
                        />
                    </div>
                )}

                {!(this.type === 'generical') && (
                    <div className="flex justify-center space-x-4 items-center mt-4">
                        <div className="flex space-x-4 items-center border border-gray-300 rounded">
                            <button
                                type="button"
                                onClick={() => { window.confirm("Change status of block " + this.fragments[0].value + "?") && this.setStatus() }}
                                className="px-4 py-2 font-medium text-white bg-blue-500 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            >
                                Change status
                            </button>
                            <input
                                type="email"
                                name="email"
                                id="email"
                                className="px-3 py-2 w-24 border-0 focus:outline-none"
                                onChange={(e) => this.changeStatus(e.target.value)}
                                placeholder="status"
                            />
                        </div>

                        <button
                            type="button"
                            onClick={() => { window.confirm("(In)Validate block " + this.fragments[0].value + "?") && this.validate() }}
                            className="px-4 py-2 font-medium text-white bg-blue-500 rounded hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                        >
                            (In)Validate
                        </button>
                    </div>
                )}
                {!(this.type === 'generical') && (

                    <div className="flex justify-center space-x-4 items-center mt-4">
                        <input
                            className="px-3 py-2 w-72 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-400"
                            onChange={(e) => this.changeComment(e.target.value)}
                            placeholder="comment"
                        />
                        <button
                            type="button"
                            onClick={() => { window.confirm("Set comment of block " + this.fragments[0].value + "?") && this.setComment() }}
                            className="px-4 py-2 font-medium text-white bg-blue-500 rounded hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-400"
                        >
                            Set
                        </button>
                    </div>
                )}

                {this.type === 'fin' && (
                    <div>
                        <div className='flex justify-center space-x-4 items-center mt-4' id={`checkbox`}>
                            {this.checkboxes.map((value, index) => (
                                <div>
                                    <input type="checkbox" id={`checkbox-${index}`} value={value} onChange={this.handleCheck.bind(this, value)} />
                                    <label htmlFor={`checkbox-${index}`}>{value}</label>
                                </div>
                            ))}
                            <div>
                                <div id={`${this.fragments[0].value}-sum`}>Sum {this.sum}</div>
                                <button
                                    type="button"
                                    onClick={() => { window.confirm("Set flag of block " + this.fragments[0].value + "?") && this.setFlag() }}
                                    className="px-4 py-2 m-auto font-medium text-white bg-blue-500 rounded hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-400"
                                >
                                    Set
                                </button>
                            </div>
                        </div>


                    </div>
                )}

                <div className="flex mt-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-1/3 p-4 border-r border-gray-200">
                        {this.fragments.map((obj) => (
                            <div key={obj.item} className="mb-4 p-2 border-b border-gray-300">
                                <p className="text-orange-900 font-semibold mb-2">{obj.item}</p>
                                {obj.value.toString().includes(".fits") ||
                                    obj.value.toString().includes(".cat") ||
                                    obj.value.toString().includes(".file") ? (
                                    <a
                                        className="text-xs text-blue-600 hover:underline"
                                        href={`${process.env.REACT_APP_SERVER_IP}/media/${obj.value.toString()}`}
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                                        </svg>

                                    </a>
                                ) : (
                                    <p className="text-xs text-gray-600">{obj.value !== null && obj.value.toString()}</p>
                                )}
                            </div>
                        ))}
                    </div>

                    <div className="w-2/3 p-4">
                        <Tabs>
                            <TabList className="flex mb-4 border-b">
                                {this.tabs.map((item) => (
                                    <Tab key={item} className="mr-4 pb-2 cursor-pointer font-semibold text-gray-600 hover:text-gray-900">
                                        {item}
                                    </Tab>
                                ))}
                            </TabList>
                            {this.tabsContent.map((value, index) => (
                                <TabPanel key={index}>
                                    <div className="relative w-full h-full overflow-hidden" onClick={() => this.panZoomRef.current.reset()}>
                                        <PanZoom ref={this.panZoomRef} onStateChange={this.handleStateChange}>
                                            <img src={`${process.env.REACT_APP_SERVER_IP}/media/${value}`} alt={value} style={{ width: '100%', height: 'auto' }} />
                                        </PanZoom>
                                    </div>
                                </TabPanel>
                            ))}
                        </Tabs>
                    </div>
                </div>






                {!(this.type === 'individual' || this.type === 'generical') && (
                    <div>
                        <div className="flex justify-center space-x-4 items-center mt-4">
                            <p className="px-4 py-2 bg-gray-200 rounded">Status of all linked objects</p>
                            <input
                                className="px-3 py-2 w-24 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
                                onChange={(e) => this.changeSubStatus(e.target.value)}
                                placeholder="status"
                            />
                            <button
                                type="button"
                                onClick={() => { window.confirm("Change status of block " + this.fragments[0].value + "?") && this.setSubStatus() }}
                                className="px-4 py-2 font-medium text-white bg-blue-500 rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
                            >
                                Change
                            </button>
                        </div>

                        <div className="flex justify-center space-x-4 items-center mt-4 mb-4">
                            <p className="px-4 py-2 bg-gray-200 rounded">Add or Remove linked objects by ID</p>
                            <input
                                className="px-3 py-2 w-24 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                onChange={(e) => this.changeTargetId(e.target.value)}
                                placeholder="status"
                            />
                            <button
                                type="button"
                                onClick={() => { window.confirm("Change status of block " + this.fragments[0].value + "?") && this.add() }}
                                className="px-4 py-2 font-medium text-white bg-blue-500 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            >
                                Add
                            </button>

                            <button
                                type="button"
                                onClick={() => { window.confirm("Change status of block " + this.fragments[0].value + "?") && this.remove() }}
                                className="px-4 py-2 font-medium text-white bg-red-500 rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400"
                            >
                                Remove
                            </button>
                        </div>
                    </div>
                )}



                <div>
                    {this.aditionals.map((obj, index) => (
                        <div key={index}>
                            {obj}
                        </div>
                    ))}
                </div>
            </div>
        )
    }
}
