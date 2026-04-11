import { Pill } from "@/components/atoms/Pill";
import { AdminMetricsGrid, PanelShell } from "@/components/organisms/AdminSections";
import { DataTable, type DataTableColumn } from "@/components/molecules/DataTable";
import { AdminConsoleTemplate } from "@/components/templates/AdminConsoleTemplate";
import { allAdminUsers, type AdminUserRow } from "@/data/mockData";

const columns: Array<DataTableColumn<AdminUserRow>> = [
  { key: "name", header: "이름", render: (row) => row.name },
  { key: "email", header: "이메일", render: (row) => row.email },
  {
    key: "role",
    header: "권한",
    render: (row) => {
      const tone = row.role === "admin" ? "info" : row.role === "owner" ? "highlight" : "neutral";
      return <Pill tone={tone}>{row.role}</Pill>;
    },
    align: "center",
  },
  { key: "phone", header: "전화번호", render: (row) => row.phone ?? "-" },
  { key: "joined", header: "가입일", render: (row) => row.joined, align: "right" },
];

function AdminUsersPage() {
  return (
    <AdminConsoleTemplate
      title="회원 관리"
      description="권한, 연락처, 가입일 기준으로 사용자 목록을 정리했습니다."
    >
      <AdminMetricsGrid />
      <PanelShell
        title="가입자 목록"
        description="리뷰닥터 가입자 목록을 table molecule 기반으로 일관되게 렌더링합니다."
      >
        <DataTable columns={columns} rows={allAdminUsers} rowKey={(row) => row.email} />
      </PanelShell>
    </AdminConsoleTemplate>
  );
}

export default AdminUsersPage;
