
function Link(props) {
	return (
		<a {...props} className='text-white font-semibold text-xl'>
			{props.children}
		</a>
	)
}

export default Link