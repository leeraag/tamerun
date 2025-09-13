import type { AxiosResponse } from "axios";
import { getFileName } from "./getFileName";

export const downloadFile = (response: AxiosResponse) => {
    const filename = getFileName(response);
    const url = window.URL.createObjectURL(response.data);
    const link = document.createElement('a');

    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
};