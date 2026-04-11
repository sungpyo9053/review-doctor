import type { ReactNode } from "react";
import { Div, Table, Tbody, Td, Th, Thead, Tr } from "../atoms/html";
import { cx } from "../../utils/cx";
import styles from "./DataTable.module.css";

export interface DataTableColumn<T> {
  key: string;
  header: string;
  render: (row: T) => ReactNode;
  align?: "left" | "center" | "right";
}

interface DataTableProps<T> {
  columns: Array<DataTableColumn<T>>;
  rows: T[];
  rowKey: (row: T) => string | number;
  emptyMessage?: string;
}

export function DataTable<T>({
  columns,
  rows,
  rowKey,
  emptyMessage = "표시할 데이터가 없습니다.",
}: DataTableProps<T>) {
  return (
    <Div className={styles.scroll}>
      <Table className={styles.table}>
        <Thead>
          <Tr>
            {columns.map((column) => (
              <Th
                key={column.key}
                className={cx(
                  column.align === "right" && styles.alignRight,
                  column.align === "center" && styles.alignCenter,
                )}
              >
                {column.header}
              </Th>
            ))}
          </Tr>
        </Thead>
        <Tbody>
          {rows.length > 0 ? (
            rows.map((row) => (
              <Tr key={rowKey(row)}>
                {columns.map((column) => (
                  <Td
                    key={column.key}
                    className={cx(
                      column.align === "right" && styles.alignRight,
                      column.align === "center" && styles.alignCenter,
                    )}
                  >
                    {column.render(row)}
                  </Td>
                ))}
              </Tr>
            ))
          ) : (
            <Tr>
              <Td className={styles.empty} colSpan={columns.length}>
                {emptyMessage}
              </Td>
            </Tr>
          )}
        </Tbody>
      </Table>
    </Div>
  );
}
