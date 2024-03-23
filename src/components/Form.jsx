import { useForm } from "react-hook-form"
import Input from './Input'
import PassInput from './PassInput'

function Form() {
	const { 
		register, 
		handleSubmit, 
		watch, 
		formState: {errors}
	 } = useForm()
	const onSubmit = data => {
		data.preventDefault()
		console.log(data)
	}

	return (
		<form onSubmit={onSubmit} className='flex flex-col gap-4 bg-white p-8 rounded-lg w-[45vw] max-w-[24rem]'>
			<div className='flex flex-col gap-4'>
				<Input placeholder='Псевдоним' {...register('username')} />
				<Input type='email' placeholder='Почта' {...register('email')} />
				<PassInput placeholder='Пароль' {...register('password')} />
			</div>
			<input type="submit" value="Подтвердить" className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md' />
		</form>
	)
}

export default Form