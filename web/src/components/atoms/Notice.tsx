import type { HTMLAttributes } from "react";
import { cx } from "../../utils/cx";
import { Div } from "./html";
import styles from "./Notice.module.css";

type NoticeTone = "info" | "success" | "error";

interface NoticeProps extends HTMLAttributes<HTMLDivElement> {
  tone?: NoticeTone;
}

export function Notice({ tone = "info", className, ...props }: NoticeProps) {
  return <Div className={cx(styles.notice, styles[tone], className)} {...props} />;
}
