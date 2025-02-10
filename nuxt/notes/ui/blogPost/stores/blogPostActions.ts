import * as axiosUtility from "../../utility/axiosInstance"

export const blogPostAction = {
  async requestPostList(payload) {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

    const { page, perPage } = payload

    try {
        const res = await djangoAxiosInstance.get(`/blog-post/list?page=${page}&perPage=${perPage}`);

        const { dataList, totalItems, totalPages } = res.data;
        console.log(`blogPostList: ${dataList}, totalItems: ${totalItems}, totalPages: ${totalPages}`)

        // 데이터 설정
        this.blogPostList = dataList || [];
        this.totalPages = totalPages || 0;
        this.totalItems = totalItems || 0;
        this.currentPage = page;
    } catch (error) {
        console.error("requestPostList() 중 에러:", error);

        // 에러가 발생하면 상태를 초기화
        this.blogPostList = [];
        this.totalPages = 0;
        this.totalItems = 0;
        this.currentPage = 1;
    }
  },

  async requestRegisterPost(payload) {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
    const { title, content } = payload; // ✅ content가 파일명인지 확인
    const userToken = localStorage.getItem("userToken");

    if (!userToken) {
      console.error("❌ 사용자 토큰이 없습니다.");
      throw new Error("로그인이 필요합니다.");
    }

    console.log("🚀 Registering Post: ", { title, content });

    try {
      const response = await djangoAxiosInstance.post("/blog-post/create", {
        title,
        content, // ✅ "title-uuid.html"이 전달되는지 확인
        userToken,
      });

      console.log("✅ 포스트 등록 성공:", response.data);
    } catch (error) {
      console.error("❌ 포스트 등록 실패:", error);
      throw new Error("포스트 등록 실패");
    }
  },

  async requestReadPost(postId) {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

    try {
      const res = await djangoAxiosInstance.get(`/blog-post/read/${postId}`);
      console.log("✅ 게시글 상세 조회 성공:", res.data);

      this.blogPost = res.data;
      this.blogPostContent = res.data.content
      return res.data;
    } catch (error) {
      console.error("❌ requestReadPost() 중 에러:", error);
      throw new Error("게시글 불러오기 실패");
    }
  }
}