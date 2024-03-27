import { useForm } from 'react-hook-form'
import Form from './Form'
import Input from './Input'
import PassInput from './PassInput'

function RegisterPage() {
	const methods = useForm()

	const submit = data => {
		console.log(data)
	}
	const isUsername = data => {
		return data.length >= 3 && data.length <= 20
	}
	const isEmail = data => {
		return true
	}
	const isPassword = data => {
		return true
	}

	return (
		<Form methods={methods} submit={submit}>
			<div className='flex flex-col gap-4'>
				<Input placeholder='Псевдоним' name='username' validate={isUsername} required />
				<Input placeholder='Почта' name='email' validate={isEmail} required />
				<PassInput placeholder='Пароль' name='password' validate={isPassword} required />
			</div>
			<input type="submit" value="Подтвердить" className='w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md' />
		</Form>
	)
}

export default RegisterPage