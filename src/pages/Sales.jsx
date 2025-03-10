import { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "sonner";
import Table from "../components/Table";
import Modal from "../components/Modal";

const API_URL = `${import.meta.env.VITE_BACKEND_URL || ""}/api/sales`;

const SalesPage = () => {
  const [sales, setSales] = useState([]);
  const [filteredSales, setFilteredSales] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);
  const [editData, setEditData] = useState(null);

  // Filters
  const [searchName, setSearchName] = useState("");
  const [selectedMode, setSelectedMode] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [availableModes, setAvailableModes] = useState([]);

  const defaultFormData = {
    item_id: "",
    item_name: "",
    selling_price: "",
    cost_price: "",
    mode: "",
    cust_name: "",
    order_date: new Date().toISOString().split("T")[0],
    stitching: false,
    expected_date: "",
    shipping: "",
    cust_address: "",
    additional_details: "",
  };

  const [formData, setFormData] = useState(defaultFormData);

  // Fetch sales data
  const fetchSales = () => {
    setLoading(true);
    axios
      .get(API_URL)
      .then((response) => {
        const salesData = response.data.data || [];
        // Sort by order_date in descending order (newest first)
        const sortedSales = salesData.sort(
          (a, b) => new Date(b.order_date) - new Date(a.order_date)
        );
        setSales(sortedSales);
        setFilteredSales(sortedSales);
        
        // Extract unique modes for the filter dropdown
        const modes = [...new Set(sortedSales.map(sale => sale.mode))].filter(Boolean);
        setAvailableModes(modes);
        
        setLoading(false);
      })
      .catch((error) => {
        setError(`Failed to fetch sales data: ${error.message}`);
        setLoading(false);
        toast.error("Failed to load sales data");
      });
  };

  useEffect(() => {
    fetchSales();
  }, []);

  useEffect(() => {
    let filteredData = sales;
    if (searchName) {
      filteredData = filteredData.filter((sale) =>
        sale.cust_name.toLowerCase().includes(searchName.toLowerCase())
      );
    }
    if (selectedMode) {
      filteredData = filteredData.filter((sale) => sale.mode === selectedMode);
    }
    if (startDate && endDate) {
      filteredData = filteredData.filter((sale) => {
        const saleDate = new Date(sale.order_date);
        return saleDate >= new Date(startDate) && saleDate <= new Date(endDate);
      });
    }
    setFilteredSales(filteredData);
  }, [searchName, selectedMode, startDate, endDate, sales]);

  const handleDelete = async (sale) => {
    try {
      await axios.delete(`${API_URL}/${sale.item_id}`);
      fetchSales();
      toast.success("Sale deleted successfully!");
    } catch (error) {
      toast.error(`Failed to delete sale: ${error.message}`);
    }
  };

  const handleEdit = (sale) => {
    setEditData(sale);
    setFormData({
      ...sale,
      selling_price: sale.selling_price?.toString() || "",
      cost_price: sale.cost_price?.toString() || "",
      order_date: sale.order_date
        ? new Date(sale.order_date).toISOString().split("T")[0]
        : "",
      expected_date: sale.expected_date
        ? new Date(sale.expected_date).toISOString().split("T")[0]
        : "",
    });
    setOpen(true);
  };

  const handleAddNew = () => {
    setEditData(null);
    setFormData(defaultFormData);
    setOpen(true);
  };

  const handleSubmit = async () => {
    const processedData = {
      ...formData,
      selling_price: parseFloat(formData.selling_price) || 0,
      cost_price: parseFloat(formData.cost_price) || 0,
      stitching: Boolean(formData.stitching),
      // Convert empty date strings to null
      expected_date: formData.expected_date === "" ? null : formData.expected_date
    };

    // Remove any computed fields that shouldn't be sent to the server
    delete processedData.margin;

    try {
      if (editData) {
        await axios.put(`${API_URL}/${editData.item_id}`, processedData);
        toast.success("Sale updated successfully!");
      } else {
        await axios.post(API_URL, processedData);
        toast.success("Sale added successfully!");
      }

      fetchSales();
      setOpen(false);
      setEditData(null);
      setFormData(defaultFormData);
    } catch (error) {
      toast.error(`Failed to save sale: ${error.message}`);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const clearFilters = () => {
    setSearchName("");
    setSelectedMode("");
    setStartDate("");
    setEndDate("");
  };

  const columns = [
    { key: "item_id", label: "Item ID" },
    { key: "item_name", label: "Item Name" },
    { key: "cust_name", label: "Customer Name" },
    { key: "mode", label: "Mode" },
    {
      key: "selling_price",
      label: "Selling Price",
      render: (row) => `₹${row.selling_price || 0}`,
    },
    {
      key: "cost_price",
      label: "Cost Price",
      render: (row) => `₹${row.cost_price || 0}`,
    },
    {
      key: "margin",
      label: "Margin",
      render: (row) => `₹${(row.selling_price || 0) - (row.cost_price || 0)}`,
    },
    { key: "order_date", label: "Order Date" },
    { key: "expected_date", label: "Expected Date" },
    {
      key: "stitching",
      label: "Stitching",
      render: (row) => (row.stitching ? "Yes" : "No"),
    },
    { key: "shipping", label: "Shipping" },
    { key: "cust_address", label: "Customer Address" },
    { key: "additional_details", label: "Additional Details" },
  ];

  const formFields = [
    { key: "item_id", label: "Item ID", type: "text" },
    { key: "item_name", label: "Item Name", type: "text" },
    { key: "selling_price", label: "Selling Price", type: "number" },
    { key: "cost_price", label: "Cost Price", type: "number" },
    { key: "mode", label: "Mode", type: "text" },
    { key: "cust_name", label: "Customer Name", type: "text" },
    { key: "order_date", label: "Order Date", type: "date" },
    { key: "expected_date", label: "Expected Date", type: "date" },
    { key: "stitching", label: "Stitching", type: "checkbox" },
    { key: "shipping", label: "Shipping", type: "text" },
    { key: "cust_address", label: "Customer Address", type: "text" },
    {
      key: "additional_details",
      label: "Additional Details",
      type: "textarea",
    },
  ];

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-xl font-bold mb-4">Sales</h1>

      {/* Filters Section */}
      <div className="bg-gray-100 p-4 mb-4 rounded">
        <h2 className="font-semibold mb-3">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Customer Name Search */}
          <div>
            <label className="block text-sm font-medium mb-1">Customer Name</label>
            <input
              type="text"
              className="w-full p-2 border rounded"
              placeholder="Search by name"
              value={searchName}
              onChange={(e) => setSearchName(e.target.value)}
            />
          </div>

          {/* Mode Filter */}
          <div>
            <label className="block text-sm font-medium mb-1">Mode</label>
            <select
              className="w-full p-2 border rounded"
              value={selectedMode}
              onChange={(e) => setSelectedMode(e.target.value)}
            >
              <option value="">All Modes</option>
              {availableModes.map((mode) => (
                <option key={mode} value={mode}>
                  {mode}
                </option>
              ))}
            </select>
          </div>

          {/* Date Range Filter */}
          <div>
            <label className="block text-sm font-medium mb-1">Start Date</label>
            <input
              type="date"
              className="w-full p-2 border rounded"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">End Date</label>
            <input
              type="date"
              className="w-full p-2 border rounded"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
        </div>
        <div className="mt-3 flex justify-end">
          <button
            className="bg-gray-500 text-white px-3 py-1 rounded"
            onClick={clearFilters}
          >
            Clear Filters
          </button>
        </div>
      </div>

      <div className="flex justify-between mb-4">
        <button
          onClick={handleAddNew}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Add Sale
        </button>
        <div className="text-sm text-gray-600">
          Showing {filteredSales.length} of {sales.length} sales
        </div>
      </div>

      {loading ? (
        <p>Loading sales data...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <Table
          columns={columns}
          data={filteredSales}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}

      {/* Modal for adding/editing sales */}
      {open && (
        <Modal
          title={editData ? "Edit Sale" : "Add Sale"}
          isOpen={open}
          onClose={() => {
            setOpen(false);
            setEditData(null);
            setFormData(defaultFormData);
          }}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {formFields.map(({ key, label, type }) => (
              <div key={key} className="mb-2">
                <label className="block text-sm font-medium mb-1">
                  {label}
                </label>
                {type === "textarea" ? (
                  <textarea
                    className="w-full p-2 border rounded"
                    name={key}
                    value={formData[key] || ""}
                    onChange={handleInputChange}
                    placeholder={label}
                    rows={3}
                  />
                ) : type === "checkbox" ? (
                  <input
                    type="checkbox"
                    name={key}
                    checked={Boolean(formData[key])}
                    onChange={handleInputChange}
                    className="ml-2"
                  />
                ) : (
                  <input
                    className="w-full p-2 border rounded"
                    name={key}
                    type={type}
                    value={formData[key] || ""}
                    onChange={handleInputChange}
                    placeholder={label}
                  />
                )}
              </div>
            ))}
          </div>
          <div className="mt-4 flex justify-end">
            <button
              className="bg-gray-500 text-white px-4 py-2 mr-2 rounded"
              onClick={() => {
                setOpen(false);
                setEditData(null);
                setFormData(defaultFormData);
              }}
            >
              Cancel
            </button>
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded"
              onClick={handleSubmit}
            >
              Save
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default SalesPage;