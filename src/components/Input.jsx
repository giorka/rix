import { useForm, useFormContext } from 'react-hook-form'

function Input({ required, name, validate = null, ...props}) {
	const { register } = useFormContext()
	const defaultValidate = data => {
		return data.length > 0
	}
	console.log(props)
	return (
		<input {...props} {...register(name, {required: required, validate: validate || defaultValidate})} className='text-black bg-[#E8ECF4] border rounded-md py-2 px-4' />
	)
}

export default Input