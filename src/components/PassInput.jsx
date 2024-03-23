import { useState } from 'react'
import Input from './Input'
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/solid'

function PassInput(props) {
	const [visible, setVisible] = useState(false)
	
	const passVisibleHandler = () => {
		setVisible(!visible)
	}

	return (
		<div className='flex flex-col relative'>
			<Input type={!visible ? 'password' : 'text'} {...props} />
			{visible ?
			<EyeIcon onClick={passVisibleHandler} className='h-6 w-6 text-gray-600 absolute top-2 right-3 cursor-pointer' /> 
			:
			<EyeSlashIcon onClick={passVisibleHandler} className='h-6 w-6 text-gray-600 absolute top-2 right-3 cursor-pointer' />}
		</div>
	)
}

export default PassInput