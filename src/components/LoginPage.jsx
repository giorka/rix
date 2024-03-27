import { useForm } from 'react-hook-form'
import Form from './Form'
import Input from './Input'
import PassInput from './PassInput'

function LoginPage() {
	const methods = useForm()

	const submit = data => {
		console.log(data)
	}

	return (
		<Form methods={methods} submit={submit}>
			<div className='flex flex-col gap-4'>
				<Input placeholder='Псевдоним' name='username' required />
				<PassInput placeholder='Пароль' name='password' required />
			</div>
			<input type="submit" value="Подтвердить" className='w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md' />
		</Form>
	)
}

export default LoginPage