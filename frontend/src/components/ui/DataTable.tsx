import React from 'react';

export interface Column<T> {
  header: string;
  accessorKey?: keyof T;
  cell?: (item: T) => React.ReactNode;
  align?: 'left' | 'center' | 'right';
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (item: T) => string;
  onRowClick?: (item: T) => void;
  emptyState?: React.ReactNode;
  className?: string;
}

export function DataTable<T>({
  columns,
  data,
  keyExtractor,
  onRowClick,
  emptyState,
  className = '',
}: DataTableProps<T>) {
  if (data.length === 0 && emptyState) {
    return <div className="w-full">{emptyState}</div>;
  }

  return (
    <div className={`w-full overflow-x-auto bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] ${className}`}>
      <table className="w-full border-collapse text-left">
        <thead>
          <tr className="bg-[#FAFAFA] border-b border-[#E5E5E5] text-[#525252] text-xs font-medium font-sans">
            {columns.map((col, idx) => (
              <th
                key={idx}
                className={`py-2.5 px-3.5 ${
                  col.align === 'right' ? 'text-right' : col.align === 'center' ? 'text-center' : 'text-left'
                } ${col.className || ''}`}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-[#E5E5E5] text-[13px] font-sans">
          {data.map((item) => (
            <tr
              key={keyExtractor(item)}
              onClick={() => onRowClick && onRowClick(item)}
              className={`transition-colors duration-100 ${
                onRowClick ? 'cursor-pointer hover:bg-[#F5F5F5]' : 'hover:bg-[#FAFAFA]'
              }`}
            >
              {columns.map((col, colIdx) => {
                const content = col.cell
                  ? col.cell(item)
                  : col.accessorKey
                  ? String(item[col.accessorKey] ?? '—')
                  : null;

                return (
                  <td
                    key={colIdx}
                    className={`py-3 px-3.5 text-[#171717] ${
                      col.align === 'right'
                        ? 'text-right'
                        : col.align === 'center'
                        ? 'text-center'
                        : 'text-left'
                    } ${col.className || ''}`}
                  >
                    {content}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
