<template>
    <client-only>
        <v-container>
            <v-card>
                <v-card-title>블로그 포스트 작성</v-card-title>
                <v-card-text>
                    <v-text-field v-model="title" label="제목" outlined></v-text-field>

                    <div class="editor-container" v-if="QuillEditor">
                        <QuillEditor
                            v-model:content="content"
                            :options="editorOptions"
                            toolbar="full"
                            ref="quillEditorRef"
                        />
                    </div>

                    <v-btn color="primary" class="mt-3" @click="submitPost">등록</v-btn>
                </v-card-text>
            </v-card>
        </v-container>
    </client-only>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useBlogPostStore } from "~/stores/blogPostStore";
import { PutObjectCommand } from "@aws-sdk/client-s3";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import { useRuntimeConfig } from "nuxt/app";
import { v4 as uuidv4 } from 'uuid';
import { createAwsS3Instance } from '~/utility/awsS3Instance';
import { compressHTML } from '~/utility/compression'; // ✅ HTML 압축 유틸리티 추가

const title = ref("");
const content = ref("");
const router = useRouter();
const blogPostStore = useBlogPostStore();
const editorOptions = ref({
    theme: "snow",
    placeholder: "Write here...",
});

const config = useRuntimeConfig();
const QuillEditor = ref(null);
const quillEditorRef = ref(null);

onMounted(async () => {
    console.log("Mounted: Dynamically loading QuillEditor...");
    const { QuillEditor: LoadedQuillEditor } = await import("@vueup/vue-quill");
    QuillEditor.value = LoadedQuillEditor;
    console.log("Mounted: QuillEditor loaded successfully.");
});

const slugify = (str: string) => {
    return str
        .toLowerCase()
        .replace(/[^\w\s-]/g, "")
        .replace(/[\s_-]+/g, "-")
        .replace(/^-+|-+$/g, "");
};

// 🚀 S3 업로드 (HTML 압축 적용)
const uploadToS3 = async (content: string, title: string) => {
    const s3Client = createAwsS3Instance();
    const uniqueId = uuidv4(); // 고유 ID 생성
    const filename = `${slugify(title)}-${uniqueId}.html`; // title-uuid.html 형식 유지

    const params = {
        Bucket: config.public.AWS_BUCKET_NAME,
        Key: `blog-post/${filename}`, // 개선된 파일명 적용
        Body: content, // 여기에 HTML 문자열을 그대로 전달
        ContentType: "text/html",
    };

    console.log("📝 S3 Upload Params:", params); // 업로드 전 확인 로그

    try {
        const data = await s3Client.send(new PutObjectCommand(params));
        console.log("✅ Content uploaded to S3:", data);
        return filename; // "title-uuid.html" 반환
    } catch (err) {
        console.error("❌ Error uploading content to S3", err);
        throw new Error("S3 업로드 실패");
    }
};

// 🚀 블로그 포스트 제출
const submitPost = async () => {
    console.log("🚀 Submit post started...");

    if (!title.value || !content.value) {
        alert("제목과 내용을 입력하세요.");
        return;
    }

    await nextTick(async () => {
        const quillInstance = quillEditorRef.value?.getQuill();
        if (!quillInstance) {
            console.error("❌ Quill instance is not available.");
            return;
        }

        const contentHtmlString = quillInstance.root.innerHTML;
        console.log("📄 HTML content to upload:", contentHtmlString);

        if (!contentHtmlString) {
            console.error("❌ Failed to extract content from QuillEditor.");
            return;
        }

        // HTML 압축 적용 (await 사용)
        const compressedHTML = await compressHTML(contentHtmlString);  // await 추가
        console.log("📄 압축된 HTML:", compressedHTML);

        try {
            const filename = await uploadToS3(compressedHTML, title.value);
            console.log("✅ File uploaded successfully, key:", filename);

            await blogPostStore.requestRegisterPost({
                title: title.value,
                content: filename
            });

            alert("블로그 포스트가 등록되었습니다!");
            router.push("/blog-post/list");
        } catch (error) {
            console.error("❌ 블로그 포스트 등록 실패:", error);
            alert("포스트 등록 중 오류가 발생했습니다.");
        }
    });
};

</script>

<style scoped>
:deep(.ql-editor) {
    min-height: 200px;
}
:deep(.ql-toolbar.ql-snow) {
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}
:deep(.ql-container.ql-snow) {
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
}
</style>
