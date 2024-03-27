import { FormProvider, useForm } from "react-hook-form"
import AuthNavigation from './AuthNavigation'

function Form({ children, methods, submit }) {
	return (
		<div className='relative'>
			<AuthNavigation />
			<FormProvider {...methods}>
				<form onSubmit={methods.handleSubmit(submit)} className='flex flex-col gap-4 bg-white p-8 rounded-lg w-[45vw] max-w-[24rem]'>
					{children}
				</form>
			</FormProvider>
		</div>
	)
}

export default Form