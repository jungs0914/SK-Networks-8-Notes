import * as axiosUtility from "../../utility/axiosInstance"

export const githubAuthenticationAction = {
    async requestGithubLoginToFiber(): Promise<void> {
        console.log("requestGithubLoginToFiber")
        const { fiberAxiosInstance } = axiosUtility.createAxiosInstances()

        try {
            return fiberAxiosInstance.get('/github-oauth/request-login-url').then((res) => {
                console.log(`res: ${res}`)
                window.location.href = res.data.url
            })
        } catch (error) {
            console.log('requestGithubLoginToFiber() 중 에러:', error)
        }
    },
    async requestAccessToken(code: string): Promise<string | null> {
        const { fiberAxiosInstance } = axiosUtility.createAxiosInstances();
        try {
            const response = await fiberAxiosInstance.post('/github-oauth/redirect-access-token', code)
            return response.data.userToken
        } catch(error){
            console.log('Access Token 요청 중 문제 발생:', error)
            throw error
        }
    },


    async requestLogout(userToken: string): Promise<void> {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances()

        try {
            await djangoAxiosInstance.post('/authentication/logout', { userToken })
        } catch (error) {
            console.log('requestLogout() 중 에러:', error)
        }
    },
    async requestValidationUserToken(userToken: string): Promise<boolean> {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances()

        try {
            const response = await djangoAxiosInstance.post('/authentication/validation', { userToken })

            if (response.data && response.data.valid !== undefined) {
                return response.data.valid;
            } else {
                console.error('Invalid response structure:', response.data);
                return false;
            }
        } catch (error) {
            console.log('requestLogout() 중 에러:', error)
            return false
        }
    }
}