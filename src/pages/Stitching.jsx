import { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "sonner";
import Table from "../components/Table";
import Modal from "../components/Modal";

const API_URL = `${import.meta.env.VITE_BACKEND_URL || ""}/api/stitching`;

const StitchingPage = () => {
  const [stitchingOrders, setStitchingOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);
  const [editData, setEditData] = useState(null);

  // Filters
  const [searchName, setSearchName] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // Status options calculated from dates
  const statusOptions = ["In Progress", "Expired"];

  const defaultFormData = {
    stitching_id: "",
    item_id: "",
    item_name: "",
    cust_name: "",
    stitching_preference: "",
    tailor_price: "",
    selling_price: "",
    order_date: new Date().toISOString().split("T")[0],
    expected_date: "",
    additional_details: "",
  };

  const [formData, setFormData] = useState(defaultFormData);

  // Calculate status based on dates
  const calculateStatus = (orderDate, expectedDate) => {
    const currentDate = new Date();
    const expDate = new Date(expectedDate);
    
    if (!expectedDate) return "In Progress";
    return currentDate > expDate ? "Expired" : "In Progress";
  };

  // Add calculated status to order data
  const processOrderData = (orders) => {
    return orders.map(order => ({
      ...order,
      status: calculateStatus(order.order_date, order.expected_date)
    }));
  };

  // Fetch stitching orders data
  const fetchStitchingOrders = () => {
    setLoading(true);
    axios
      .get(API_URL)
      .then((response) => {
        const ordersData = response.data.data || [];
        // Sort by order_date in descending order (newest first)
        const sortedOrders = ordersData.sort(
          (a, b) => new Date(b.order_date) - new Date(a.order_date)
        );
        // Add calculated status
        const processedOrders = processOrderData(sortedOrders);
        setStitchingOrders(processedOrders);
        setFilteredOrders(processedOrders);
        setLoading(false);
      })
      .catch((error) => {
        setError(`Failed to fetch stitching orders: ${error.message}`);
        setLoading(false);
        toast.error("Failed to load stitching orders");
      });
  };

  useEffect(() => {
    fetchStitchingOrders();
  }, []);

  useEffect(() => {
    let filteredData = stitchingOrders;
    if (searchName) {
      filteredData = filteredData.filter((order) =>
        order.cust_name.toLowerCase().includes(searchName.toLowerCase())
      );
    }
    if (selectedStatus) {
      filteredData = filteredData.filter((order) => order.status === selectedStatus);
    }
    if (startDate && endDate) {
      filteredData = filteredData.filter((order) => {
        const orderDate = new Date(order.order_date);
        return orderDate >= new Date(startDate) && orderDate <= new Date(endDate);
      });
    }
    setFilteredOrders(filteredData);
  }, [searchName, selectedStatus, startDate, endDate, stitchingOrders]);

  const handleDelete = async (order) => {
    try {
      await axios.delete(`${API_URL}/${order.stitching_id}`);
      fetchStitchingOrders();
      toast.success("Stitching order deleted successfully!");
    } catch (error) {
      toast.error(`Failed to delete stitching order: ${error.message}`);
    }
  };

  const handleEdit = (order) => {
    setEditData(order);
    setFormData({
      ...order,
      tailor_price: order.tailor_price?.toString() || "",
      selling_price: order.selling_price?.toString() || "",
      order_date: order.order_date
        ? new Date(order.order_date).toISOString().split("T")[0]
        : "",
      expected_date: order.expected_date
        ? new Date(order.expected_date).toISOString().split("T")[0]
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
    // Validate required fields
    if (!formData.item_name || !formData.cust_name) {
      toast.error("Please fill in all required fields.");
      return;
    }
  
    const processedData = {
      ...formData,
      item_id: formData.item_id === "" ? null : formData.item_id, // Set item_id to null if it's an empty string
      tailor_price: formData.tailor_price ? parseFloat(formData.tailor_price) : null,
      selling_price: formData.selling_price ? parseFloat(formData.selling_price) : null,
      expected_date: formData.expected_date === "" ? null : formData.expected_date,
    };
  
    // Remove any computed fields that shouldn't be sent to the server
    delete processedData.status;
    delete processedData.margin;
  
    try {
      if (editData) {
        await axios.put(`${API_URL}/${editData.stitching_id}`, processedData);
        toast.success("Stitching order updated successfully!");
      } else {
        await axios.post(API_URL, processedData);
        toast.success("Stitching order added successfully!");
      }
  
      fetchStitchingOrders();
      setOpen(false);
      setEditData(null);
      setFormData(defaultFormData);
    } catch (error) {
      console.error(error);
      toast.error(`Failed to save stitching order: ${error.message}`);
    }
  };
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const clearFilters = () => {
    setSearchName("");
    setSelectedStatus("");
    setStartDate("");
    setEndDate("");
  };

  const columns = [
    { key: "stitching_id", label: "Stitching ID" },
    { key: "item_id", label: "Item ID" },
    { key: "item_name", label: "Item Name" },
    { key: "cust_name", label: "Customer Name" },
    {
      key: "tailor_price",
      label: "Tailor Price",
      render: (row) => `₹${row.tailor_price || 0}`,
    },
    {
      key: "selling_price",
      label: "Selling Price",
      render: (row) => `₹${row.selling_price || 0}`,
    },
    {
      key: "margin",
      label: "Margin",
      render: (row) => `₹${(row.selling_price || 0) - (row.tailor_price || 0)}`,
    },
    { 
      key: "status", 
      label: "Status",
      render: (row) => {
        const status = row.status;
        const colorClass = status === "Expired" ? "text-red-600 font-medium" : "text-green-600 font-medium";
        return <span className={colorClass}>{status}</span>;
      }
    },
    { key: "order_date", label: "Order Date" },
    { key: "expected_date", label: "Expected Date" },
    { key: "stitching_preference", label: "Stitching Preference" },
    { key: "additional_details", label: "Additional Details" },
  ];

  // Dynamically determine if stitching_id should be readonly based on edit vs add mode
  const formFields = [
    ...(editData ? [{ 
        key: "stitching_id", 
        label: "Stitching ID", 
        type: "text", 
        readOnly: true  // Readonly in edit mode
      }] : []),
    { key: "item_id", label: "Item ID", type: "text" },
    { key: "item_name", label: "Item Name", type: "text" },
    { key: "cust_name", label: "Customer Name", type: "text" },
    { key: "stitching_preference", label: "Stitching Preference", type: "text" },
    { key: "tailor_price", label: "Tailor Price", type: "number" },
    { key: "selling_price", label: "Selling Price", type: "number" },
    { key: "order_date", label: "Order Date", type: "date" },
    { key: "expected_date", label: "Expected Date", type: "date" },
    {
      key: "additional_details",
      label: "Additional Details",
      type: "textarea",
    },
  ];

  const renderActionButtons = (order) => (
    <div className="flex space-x-2">
      <button
        onClick={() => handleEdit(order)}
        className="bg-blue-500 text-white px-2 py-1 rounded text-xs"
      >
        Edit
      </button>
      <button
        onClick={() => handleDelete(order)}
        className="bg-red-500 text-white px-2 py-1 rounded text-xs"
      >
        Delete
      </button>
    </div>
  );

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-xl font-bold mb-4">Stitching Management</h1>

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

          {/* Status Filter */}
          <div>
            <label className="block text-sm font-medium mb-1">Status</label>
            <select
              className="w-full p-2 border rounded"
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
            >
              <option value="">All Statuses</option>
              {statusOptions.map((status) => (
                <option key={status} value={status}>
                  {status}
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
          Add Stitching Order
        </button>
        <div className="text-sm text-gray-600">
          Showing {filteredOrders.length} of {stitchingOrders.length} orders
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-orange-500" />
        </div>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <Table
          columns={columns}
          data={filteredOrders}
          onEdit={handleEdit}
          onDelete={handleDelete}
          renderActions={renderActionButtons}
        />
      )}

      {/* Modal for adding/editing stitching orders */}
      {open && (
        <Modal
          title={editData ? "Edit Stitching Order" : "Add Stitching Order"}
          isOpen={open}
          onClose={() => {
            setOpen(false);
            setEditData(null);
            setFormData(defaultFormData);
          }}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {formFields.map(({ key, label, type, readOnly }) => (
              <div key={key} className={key === "additional_details" ? "col-span-2" : ""}>
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
                    readOnly={readOnly}
                  />
                ) : (
                  <input
                    className="w-full p-2 border rounded"
                    name={key}
                    type={type}
                    value={formData[key] || ""}
                    onChange={handleInputChange}
                    placeholder={label}
                    readOnly={readOnly}
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

export default StitchingPage;