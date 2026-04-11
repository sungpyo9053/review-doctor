import { PlaceholderPanel } from "../organisms/AdminSections";
import { AdminConsoleTemplate } from "./AdminConsoleTemplate";

interface AdminPlaceholderTemplateProps {
  title: string;
  description: string;
}

function AdminPlaceholderTemplate({
  title,
  description,
}: AdminPlaceholderTemplateProps) {
  return (
    <AdminConsoleTemplate title={title} description="추가 관리 기능을 같은 템플릿 위에 이어서 확장할 수 있습니다.">
      <PlaceholderPanel title={title} description={description} />
    </AdminConsoleTemplate>
  );
}

export default AdminPlaceholderTemplate;
