import type { AxiosResponse } from "axios";

export const getFileName = (response: AxiosResponse) => {
    const contentDispositionHeader = response.headers['content-disposition'];
    const filenameRegex = /filename\*?=['"]?(?:UTF-\d['"]*)?([^;\r\n"']*)['"]?/;
    const filename = decodeURIComponent(contentDispositionHeader.match(filenameRegex)[1]);

    return filename;
};