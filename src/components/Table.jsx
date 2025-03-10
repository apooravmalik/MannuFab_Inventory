import PropTypes from "prop-types";
import { useState, useEffect } from "react";
import { FaEllipsisV } from "react-icons/fa";

const Table = ({ 
  columns, 
  data,
  onEdit,
  onDelete
}) => {
  const [dropdownIndex, setDropdownIndex] = useState(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest('.dropdown-container')) {
        setDropdownIndex(null);
      }
    };
    
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  // Process columns to add actions if edit or delete functions are provided
  const processedColumns = [...columns];
  
  if (onEdit || onDelete) {
    // Check if an actions column already exists
    const actionsColumnIndex = processedColumns.findIndex(col => col.key === 'actions');
    
    if (actionsColumnIndex === -1) {
      // Add actions column if it doesn't exist
      processedColumns.push({
        key: 'actions',
        label: 'Actions',
        render: (row, index) => (
          <div className="relative dropdown-container">
            <button
              onClick={(e) => {
                e.stopPropagation();
                setDropdownIndex(dropdownIndex === index ? null : index);
              }}
              className="p-1"
            >
              <FaEllipsisV className="cursor-pointer text-lg" />
            </button>

            {dropdownIndex === index && (
              <div className="absolute right-0 mt-2 bg-white border rounded shadow-lg w-32 z-10">
                {onEdit && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onEdit(row);
                      setDropdownIndex(null);
                    }}
                    className="block w-full px-4 py-2 text-left hover:bg-gray-200"
                  >
                    Edit
                  </button>
                )}
                {onDelete && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (window.confirm("Are you sure you want to delete this item?")) {
                        onDelete(row);
                        setDropdownIndex(null);
                      }
                    }}
                    className="block w-full px-4 py-2 text-left text-red-600 hover:bg-gray-200"
                  >
                    Delete
                  </button>
                )}
              </div>
            )}
          </div>
        ),
      });
    }
  }

  return (
    <div className="overflow-x-auto">
      {data.length === 0 ? (
        <p>No data available.</p>
      ) : (
        <table className="w-full border-collapse border border-gray-300 text-sm">
          <thead>
            <tr className="bg-gray-100 text-left">
              {processedColumns.map((col, index) => (
                <th key={index} className="p-2 border">{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex} className="border hover:bg-gray-50">
                {processedColumns.map((col, colIndex) => (
                  <td key={colIndex} className="p-2 border">
                    {col.render ? col.render(row, rowIndex) : (row[col.key] || "N/A")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

Table.propTypes = {
  columns: PropTypes.array.isRequired,
  data: PropTypes.array.isRequired,
  onEdit: PropTypes.func,
  onDelete: PropTypes.func
};

export default Table;