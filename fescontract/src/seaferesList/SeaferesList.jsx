import React, {useEffect, useState} from "react";
import {Input, Table, Tooltip} from "antd";
import axios from "axios";

const SeaferesList = (props) => {
  const [data, setData] = useState(null)
  const [dataSource, setDataSource] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(false)
  const [value, setValue] = useState( {
    name: '',
    email: ''
  })

  useEffect(() => {
    axios('/update')
    axios('/get_data').then((data) => {
      setData(data.data)
    }).catch((e) => {
      setError(true)
      console.log(e)
    })
  }, [setData]);

  useEffect(() => {
   setDataSource(data)
  }, [data]);



  const filterInput = (field) => (
    <Input
      placeholder='Поиск'
      value={value[field]}
      onChange={e => {
        const currentValue = e.target.value.toLowerCase()
        setValue({field: currentValue})
        const filteredData = data.filter(entry => entry[field].toLowerCase().includes(currentValue))
        setDataSource(filteredData)
      }}
    />
  )

  const columns = [
    {
      title: filterInput('name'),
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: filterInput('email'),
      dataIndex: 'email',
      key: 'email'
    },
    {
      title: 'Баллы',
      dataIndex: 'points',
      key: 'points'
    },
    {
      title: 'Уровень',
      dataIndex: 'level',
      key: 'level'
    },
    {
      title: 'Тип теста',
      dataIndex: 'testType',
      key: 'testType'
    },
    {
      title: 'Дата теста',
      dataIndex: 'date',
      key: 'date',
      render: (text, record) => <Tooltip placement="right" title='YYYY-MM-DD'>{text}</Tooltip>,
      sorter: (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    },
  ]

  return <div><Table columns={columns} dataSource={dataSource}/></div>
}

export default SeaferesList;
