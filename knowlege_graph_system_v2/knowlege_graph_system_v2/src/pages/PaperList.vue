<template>
  <a-card title="文献列表" style="margin: 16px">
    <!-- 搜索条 -->
    <a-row :gutter="16" style="margin-bottom: 16px">
      <a-col :span="18">
        <a-input
          v-model:value="searchKey"
          placeholder="输入标题、作者或机构"
          allow-clear
          @pressEnter="onSearch"
        />
      </a-col>
      <a-col :span="6">
        <a-button type="primary" block @click="onSearch">搜索</a-button>
      </a-col>
    </a-row>

    <!-- 表格 -->
    <a-table
      :columns="columns"
      :data-source="data"
      :loading="loading"
      :pagination="pagination"
      row-key="id"
      @change="handleTableChange"
    >
      <!-- 标题 + 外部链接 -->
      <template #bodyCell="{ column, record }">
        <template v-if="column.dataIndex === 'title'">
          <a :href="record.url" target="_blank" rel="noopener noreferrer">
            {{ record.title }}
          </a>
        </template>
        <template v-else-if="column.dataIndex === 'authors'">
          <span>{{ record.authors.join(";") }}</span>
        </template>
      </template>
    </a-table>
  </a-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { get } from "@/api/http"; // 你的 axios 封装

/* 表格列定义 */
const columns = [
  { title: "标题", dataIndex: "title", width: 280 },
  { title: "作者", dataIndex: "authors", width: 200 },
  { title: "机构", dataIndex: "orgs", width: 160 },
  { title: "年份", dataIndex: "year", width: 80, align: "center" },
];

/* 状态 */
const loading = ref(false);
const searchKey = ref("");
const data = ref<Paper[]>([]);
const pagination = ref({ current: 1, pageSize: 10, total: 0 });

/* 类型 */
interface Paper {
  id: string;
  title: string;
  authors: string[];
  orgs: string[];
  year: number;
  url: string; // 外部原文链接
}

/* 首次加载全部 */
onMounted(() => loadData());

/* 搜索 / 分页 */
function onSearch() {
  pagination.value.current = 1;
  loadData();
}
function handleTableChange(pager: any) {
  pagination.value = pager;
  loadData();
}

async function loadData() {
  loading.value = true;
  try {
    /* 后端已经支持全文检索，把搜索框内容直接当 q 参数 */
    const res = await get("/graph/root", {
      limit: 200, // 先拉 200 条，前端再分页
      q: searchKey.value.trim(),
    });
    /* 把图节点转成 Paper 类型 */
    const papers: Paper[] = res.nodes
      .filter((n: any) => n.type === "Paper")
      .map((n: any) => ({
        id: n.id,
        title: n.title,
        authors: n.authors || [],
        orgs: n.orgs || [],
        year: n.year || 0,
        url: n.url || `https://doi.org/${n.doi}`,
      }));

    const filtered = papers; // 如需再过滤可继续
    const { current = 1, pageSize = 10 } = pagination.value;
    const start = (current - 1) * pageSize;
    data.value = filtered.slice(start, start + pageSize);
    pagination.value.total = filtered.length;
  } finally {
    loading.value = false;
  }
}
</script>
