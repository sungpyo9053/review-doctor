import { AdminMetricsGrid, PanelShell } from "@/components/organisms/AdminSections";
import { Pill } from "@/components/atoms/Pill";
import { Div, P } from "@/components/atoms/html";
import { DataTable, type DataTableColumn } from "@/components/molecules/DataTable";
import { AdminConsoleTemplate } from "@/components/templates/AdminConsoleTemplate";
import {
  recentAdminUsers,
  recentAnalysisJobs,
  type AdminUserRow,
  type AnalysisJobRow,
} from "@/data/mockData";
import styles from "./page.module.css";

const userColumns: Array<DataTableColumn<AdminUserRow>> = [
  { key: "name", header: "이름", render: (row) => row.name },
  { key: "email", header: "이메일", render: (row) => row.email },
  { key: "role", header: "유형", render: (row) => row.role },
  { key: "joined", header: "가입일", render: (row) => row.joined, align: "right" },
];

const analysisColumns: Array<DataTableColumn<AnalysisJobRow>> = [
  { key: "store", header: "가게명", render: (row) => row.store },
  { key: "reviews", header: "리뷰 수", render: (row) => row.reviews, align: "right" },
  {
    key: "status",
    header: "상태",
    render: (row) => <Pill tone={row.status === "성공" ? "positive" : "danger"}>{row.status}</Pill>,
    align: "center",
  },
  { key: "time", header: "시간", render: (row) => row.time, align: "right" },
];

function AdminDashboardPage() {
  return (
    <AdminConsoleTemplate
      title="관리자 페이지"
      description="서비스 현황과 최근 운영 로그를 한 화면에서 확인할 수 있도록 구성했습니다."
    >
      <AdminMetricsGrid />

      <Div className={styles.twoColumn}>
        <PanelShell title="최근 가입자" description="최근 가입된 사용자 흐름을 빠르게 확인하세요.">
          <DataTable
            columns={userColumns}
            rows={recentAdminUsers}
            rowKey={(row) => row.email}
          />
        </PanelShell>

        <PanelShell
          title="최근 분석 요청"
          description="성공/실패 상태와 요청 시간을 함께 추적합니다."
        >
          <DataTable
            columns={analysisColumns}
            rows={recentAnalysisJobs}
            rowKey={(row) => `${row.store}-${row.time}`}
          />
        </PanelShell>
      </Div>

      <PanelShell title="운영 메모" description="현재 구조에서 바로 확장할 수 있는 다음 단계입니다.">
        <P>
          회원, 가게, 분석, 리포트를 각각 별도 organism으로 분리해두었기 때문에 실제 API
          연결 시에도 동일한 템플릿을 유지하면서 데이터만 치환하면 됩니다.
        </P>
      </PanelShell>
    </AdminConsoleTemplate>
  );
}

export default AdminDashboardPage;
