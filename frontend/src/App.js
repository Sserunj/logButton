import React, { useState, useEffect } from 'react'
import './app.css'
import DataTable from 'react-data-table-component';
import axios from 'axios'


const titlestyle = {
  headRow: {
    style: {
      fontWeight: "bold",
      fontSize: '15px',
    },
  },
};

const rowstyles = [
  {
    when: row => row.name === 'Blendon',
    style: {
      backgroundColor: '#666563',
      color:'white'
    }
  },
  {
    when: row => row.name === 'Kabo',
    style: {
      backgroundColor: '#697a7a',
      color:'white'
    }
  }
]

const columns = [
  {
    name: 'NAME',
    selector: row => row.name,
    sortable: true,
  },
  {
    name: 'DATE',
    selector: row => row.date,
  },
  {
    name: 'TIME',
    selector: row => row.time,
  }
];


function App() {
  const [data, setData] = useState([])

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/all_logs').then((res) => {
      // console.log(res.data)
      setData(res.data)
    }).catch((err) => {
      console.log(err)
    })
  }, [])

  function handleSearch(e) {
    const newData = data.filter(row => {
      return row.name.includes(e.target.value)
    })
    setData(newData)
  }

  return (
    <>
      <div className='container'>
        <div className='app'>
          <div className='title'>FARM DATE-TIME LOGGER</div>
          <div className="text-end pb-1">
          <input
            type="text"
            placeholder="search"
            onChange={handleSearch}
          />
        </div>
          <DataTable
            customStyles={titlestyle}
            columns={columns}
            data={data}
            conditionalRowStyles={rowstyles}
            pagination
            paginationRowsPerPageOptions={[10, 20, 30]}
            fixedHeader
            fixedHeaderScrollHeight="400px"
          />
        </div>
      </div>
    </>
  )
}

export default App
