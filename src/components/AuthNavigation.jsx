import Link from './Link'

function AuthNavigation() {
	return (
		<div className='w-full p-2.5 absolute bg-blue-500 -top-8 rounded-md flex justify-around'>
			<Link href="/register">Регистрация</Link>
			<Link href="/login">Вход</Link>
		</div>
	)
}

export default AuthNavigation