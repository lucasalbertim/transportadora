import { cn } from '../../utils/cn'

const buttonVariants = {
  default: "bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500",
  destructive: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
  outline: "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:ring-primary-500",
  secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500",
  ghost: "text-gray-700 hover:bg-gray-100 focus:ring-gray-500",
  link: "text-primary-600 underline-offset-4 hover:underline focus:ring-primary-500",
}

const buttonSizes = {
  default: "h-10 px-4 py-2",
  sm: "h-9 rounded-md px-3",
  lg: "h-11 rounded-md px-8",
  icon: "h-10 w-10",
}

export function Button({ 
  className, 
  variant = "default", 
  size = "default", 
  children, 
  ...props 
}) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
        buttonVariants[variant],
        buttonSizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}