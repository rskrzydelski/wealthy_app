import React from 'react'

import { BottomBelt } from './pages/css/bottom'

export default function Bottom () {
  return (
    <BottomBelt>
      <p style={copyStyle}>&copy; Developed by RS</p>
    </BottomBelt>
  )
}

const copyStyle = {
  'text-align': 'center',
  padding: '10px'
}
