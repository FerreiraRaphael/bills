import { UserButton } from "@clerk/nextjs";

export default function Home() {
  return (
    <div className="h-screen">
      cry baby
      <UserButton userProfileProps={{
        // additionalOAuthScopes: {
        //   google: [
        //     'https://www.googleapis.com/auth/gmail.readonly'
        //   ],
        // }
      }} />
    </div>
  )
}
