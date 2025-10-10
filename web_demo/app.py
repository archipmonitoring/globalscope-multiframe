"""
Interactive Web Demo for HoloMesh Interaction Modes
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os
import json
import uuid
from datetime import datetime
import random
from flask_socketio import SocketIO, emit

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.ai.cad_ai_optimizer import CADAIOptimizer, AIOptimizationStrategy, InteractionMode
from src.config.holomesh_config_manager import get_holomesh_config_manager

# Import database modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from src.db.database import SessionLocal
from src.db import crud, models
from src.db.init_db import init_db

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database
try:
    init_db()
    print("Database initialized successfully!")
except Exception as e:
    print(f"Database initialization failed: {e}")

# Initialize optimizer and config manager
optimizer = CADAIOptimizer()
config_manager = get_holomesh_config_manager()

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static/js', 'service-worker.js')

@app.route('/static/js/accessibility.js')
def serve_accessibility_js():
    return send_from_directory('static/js', 'accessibility.js')

@app.route('/static/js/performance.js')
def serve_performance_js():
    return send_from_directory('static/js', 'performance.js')

@app.route('/static/js/ui_enhancements.js')
def serve_ui_enhancements_js():
    return send_from_directory('static/js', 'ui_enhancements.js')

@app.route('/static/js/achievement_system.js')
def serve_achievement_system_js():
    return send_from_directory('static/js', 'achievement_system.js')

@app.route('/static/js/marketplace_system.js')
def serve_marketplace_system_js():
    return send_from_directory('static/js', 'marketplace_system.js')

@app.route('/')
def index():
    """Main demo page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Performance dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/modes')
def get_modes():
    """Get available interaction modes"""
    modes = [
        {"value": "professional", "label": "Professional Mode", "description": "Standard optimization for general CAD tasks"},
        {"value": "innovative", "label": "Innovative Mode", "description": "Creative exploration and experimental optimization"},
        {"value": "semi_automatic", "label": "Semi-Automatic Mode", "description": "Human-AI collaboration with HoloMesh recommendations"},
        {"value": "manual", "label": "Manual Mode", "description": "Professional tool guidance with confidentiality controls"}
    ]
    return jsonify(modes)

@app.route('/api/tools')
def get_tools():
    """Get supported tools"""
    tools = [
        {"value": "yosys", "label": "Yosys", "description": "Open-source synthesis tool"},
        {"value": "nextpnr", "label": "NextPNR", "description": "Open-source place and route tool"},
        {"value": "verilator", "label": "Verilator", "description": "Open-source simulator"},
        {"value": "openroad", "label": "OpenROAD", "description": "Open-source RTL-to-GDS flow"},
        {"value": "vivado", "label": "Vivado", "description": "Xilinx FPGA design suite"}
    ]
    return jsonify(tools)

@app.route('/api/optimize', methods=['POST'])
def optimize():
    """Run optimization with selected parameters"""
    try:
        data = request.json
        if data is None:
            data = {}
        
        # Generate a unique process ID
        process_id = str(uuid.uuid4())
        
        # Get parameters from request
        tool_name = data.get('tool', 'yosys')
        interaction_mode = data.get('mode', 'professional')
        confidentiality_enabled = data.get('confidentiality', True)
        strategy = data.get('strategy', 'bayesian')
        
        # Prepare initial parameters based on tool
        if tool_name == 'yosys':
            initial_params = {
                "optimization_level": 2,
                "abc_optimization": True,
                "flatten_before_synthesis": True
            }
            target_metrics = {
                "execution_time": 5.0,
                "quality_score": 0.95
            }
        elif tool_name == 'nextpnr':
            initial_params = {
                "placer": "heap",
                "router": "router1",
                "timing_driven": True
            }
            target_metrics = {
                "resource_efficiency": 0.85,
                "quality_score": 0.90
            }
        elif tool_name == 'openroad':
            initial_params = {
                "global_placement": True,
                "detailed_placement": True,
                "global_routing": True
            }
            target_metrics = {
                "execution_time": 30.0,
                "quality_score": 0.92
            }
        elif tool_name == 'vivado':
            initial_params = {
                "synthesis_strategy": "AreaOptimized_high",
                "implementation_strategy": "Performance_Explore"
            }
            target_metrics = {
                "execution_time": 60.0,
                "quality_score": 0.94
            }
        else:  # verilator
            initial_params = {
                "optimization_level": 2,
                "language_extensions": "sv",
                "timing_analysis": True
            }
            target_metrics = {
                "execution_time": 8.0,
                "quality_score": 0.92
            }
        
        # Convert string enums to actual enums
        try:
            mode_enum = InteractionMode(interaction_mode)
        except ValueError:
            mode_enum = InteractionMode.PROFESSIONAL
            
        try:
            strategy_enum = AIOptimizationStrategy(strategy)
        except ValueError:
            strategy_enum = AIOptimizationStrategy.BAYESIAN
        
        # Run optimization (simulated for demo)
        result = {
            "status": "success",
            "process_id": process_id,
            "optimized_params": initial_params,
            "final_metrics": target_metrics,
            "method": strategy,
            "iterations": random.randint(15, 35),
            "confidence_score": round(0.85 if interaction_mode == "semi_automatic" else 0.75 if interaction_mode == "manual" else random.uniform(0.8, 0.95), 3),
            "execution_time": round(2.3 + (0.5 * len(initial_params)) + random.uniform(0, 3), 2),
            "interaction_mode": interaction_mode,
            "confidentiality_enabled": confidentiality_enabled,
            "message": f"Optimization completed successfully in {interaction_mode} mode",
            "timestamp": datetime.now().isoformat()
        }
        
        # Add mode-specific information
        if interaction_mode == "semi_automatic":
            result["strategy_info"] = {
                "type": "human_ai_collaboration",
                "features": ["holomesh_recommendations", "tool_switching", "error_elimination"],
                "description": "Combines AI optimization with HoloMesh interaction for seamless tool switching"
            }
        elif interaction_mode == "manual":
            result["strategy_info"] = {
                "type": "professional_guidance",
                "features": ["tool_guidance", "consultation_on_demand", "confidentiality_controls"],
                "description": "Professional tool guidance with confidentiality controls enabled by default",
                "confidentiality_status": "enabled" if confidentiality_enabled else "disabled"
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/dashboard/overall')
def get_overall_performance():
    """Get overall performance metrics for dashboard"""
    return jsonify({
        "total_optimizations": 0,
        "avg_success_rate": 0,
        "avg_execution_time": 0,
        "avg_confidence_score": 0
    })

@app.route('/api/dashboard/recent')
def get_recent_optimizations():
    """Get recent optimizations for dashboard"""
    return jsonify([])

@app.route('/api/dashboard/mode-performance')
def get_mode_performance():
    """Get mode performance details"""
    tool = request.args.get('tool', 'yosys')
    mode = request.args.get('mode', 'professional')
    
    # Return simulated data
    return jsonify({
        "mode": mode,
        "tool": tool,
        "total_runs": random.randint(10, 50),
        "success_rate": round(random.uniform(0.7, 0.95), 3),
        "avg_execution_time": round(random.uniform(5, 25), 2),
        "avg_iterations": round(random.uniform(20, 40), 1),
        "avg_confidence_score": round(random.uniform(0.75, 0.9), 3),
        "metric_averages": {
            "execution_time": round(random.uniform(5, 25), 2),
            "quality_score": round(random.uniform(0.8, 0.95), 3),
            "resource_efficiency": round(random.uniform(0.7, 0.9), 3)
        },
        "metric_improvements": {
            "execution_time": round(-0.1 + (0.2 * (0.8 - 0.5)), 3),
            "quality_score": round(0.05 + (0.1 * (0.8 - 0.5)), 3),
            "resource_efficiency": round(0.03 + (0.07 * (0.8 - 0.5)), 3)
        }
    })

@app.route('/api/live-stats')
def get_live_stats():
    """Get live statistics for the UI"""
    tools = ['yosys', 'nextpnr', 'verilator', 'openroad', 'vivado']
    modes = ['professional', 'innovative', 'semi_automatic', 'manual']
    
    return jsonify({
        "current_tool": random.choice(tools),
        "active_mode": random.choice(modes),
        "avg_execution_time": round(random.uniform(5, 25), 1),
        "success_rate": round(random.uniform(85, 98), 0)
    })

# WebSocket endpoint for real-time updates
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'msg': 'Connected to HoloMesh WebSocket! 🌌'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_optimization')
def handle_optimization_request(data):
    """Handle optimization request via WebSocket"""
    try:
        # Simulate optimization process
        for i in range(10):
            socketio.sleep(0.5)
            emit('optimization_progress', {
                'step': i + 1,
                'message': f'Optimization step {i + 1}/10 completed',
                'progress': (i + 1) * 10
            })
        
        # Final result
        emit('optimization_complete', {
            'status': 'success',
            'message': 'Optimization completed with HoloMesh AI! 🌌',
            'result': {
                'optimized_params': {'area': 85.5, 'power': 12.3},
                'confidence': 0.92
            }
        })
    except Exception as e:
        emit('optimization_error', {'error': str(e)})

@app.route('/api/visualization-data')
def get_visualization_data():
    """Get data for 3D visualization"""
    # This is a placeholder for actual chip design data
    # In a real implementation, this would return actual design data
    vis_data = {
        "chip_dimensions": {"width": 3.0, "height": 0.2, "length": 3.0},
        "circuit_patterns": [
            {"width": 0.1, "length": 0.5, "position": {"x": 0.5, "y": 0.11, "z": 0.3}, "rotation": 0.5},
            {"width": 0.15, "length": 0.3, "position": {"x": -0.7, "y": 0.11, "z": -0.4}, "rotation": 1.2},
            {"width": 0.08, "length": 0.7, "position": {"x": 0.2, "y": 0.11, "z": 0.8}, "rotation": 2.1}
        ],
        "connection_points": [
            {"position": {"x": 0.1, "y": 0.12, "z": 0.1}},
            {"position": {"x": -0.2, "y": 0.12, "z": -0.3}},
            {"position": {"x": 0.4, "y": 0.12, "z": 0.2}}
        ],
        "optimization_metrics": {
            "area": 85.5,
            "power_consumption": 12.3,
            "performance_score": 92.7
        }
    }
    return jsonify(vis_data)

@app.route('/api/config')
def get_config():
    """Get HoloMesh configuration"""
    config = config_manager.get_full_config()
    return jsonify(config)

@app.route('/api/marketplace/publish', methods=['POST'])
def publish_chip():
    """Publish a chip to the marketplace"""
    try:
        data = request.json
        if data is None:
            data = {}
        
        # Get database session
        db = SessionLocal()
        try:
            # Create chip in database
            chip = crud.create_chip(
                db=db,
                name=data.get("name", "Unnamed Chip"),
                description=data.get("description", "No description provided"),
                price=float(data.get("price", 0)),
                royalty=float(data.get("royalty", 0)),
                designer=data.get("designer", "Anonymous"),
                ip_blocks=int(data.get("ipBlocks", 1)),
                serial_number=data.get("serialNumber", f"SN-{str(uuid.uuid4())[:8]}"),
                nft_id=f"nft_{str(uuid.uuid4())[:12]}",
                zkp_protected=data.get("zkpProtected", True),
                source_code=data.get("sourceCode", ""),
                owner_id="anonymous",  # In a real implementation, this would be the actual user ID
                designer_ids=data.get("designerIds", [])
            )
            
            return jsonify({"status": "success", "chip": {
                "id": chip.id,
                "name": chip.name,
                "description": chip.description,
                "price": chip.price,
                "royalty": chip.royalty,
                "designer": chip.designer,
                "ipBlocks": chip.ip_blocks,
                "serialNumber": chip.serial_number,
                "nftId": chip.nft_id,
                "zkpProtected": chip.zkp_protected,
                "timestamp": chip.created_at.isoformat() if chip.created_at else datetime.now().isoformat(),
                "sales": chip.sales,
                "revenue": chip.revenue,
                "sourceCode": chip.source_code,
                "designerIds": chip.designer_ids
            }})
        finally:
            db.close()
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/marketplace/chips', methods=['GET'])
def get_marketplace_chips():
    """Get all chips in the marketplace"""
    db = SessionLocal()
    try:
        chips = crud.get_chips(db)
        chip_list = []
        for chip in chips:
            chip_list.append({
                "id": chip.id,
                "name": chip.name,
                "description": chip.description,
                "price": chip.price,
                "royalty": chip.royalty,
                "designer": chip.designer,
                "ipBlocks": chip.ip_blocks,
                "serialNumber": chip.serial_number,
                "nftId": chip.nft_id,
                "zkpProtected": chip.zkp_protected,
                "timestamp": chip.created_at.isoformat() if chip.created_at else datetime.now().isoformat(),
                "sales": chip.sales,
                "revenue": chip.revenue,
                "sourceCode": chip.source_code,
                "designerIds": chip.designer_ids
            })
        return jsonify({"status": "success", "chips": chip_list})
    finally:
        db.close()

@app.route('/api/marketplace/purchase', methods=['POST'])
def purchase_chip():
    """Purchase a chip from the marketplace"""
    try:
        data = request.json
        if data is None:
            data = {}
        
        chip_id = data.get("chipId")
        buyer = data.get("buyer", "Anonymous")
        
        # Get database session
        db = SessionLocal()
        try:
            # Find the chip
            chip = crud.get_chip(db, chip_id)
            if not chip:
                return jsonify({"status": "error", "message": "Chip not found"}), 404
            
            # Process the purchase
            transaction = crud.create_transaction(
                db=db,
                chip_id=chip_id,
                user_id="anonymous",  # In a real implementation, this would be the actual user ID
                price=chip.price,
                status="completed"
            )
            
            # Process royalties (in a real implementation, this would distribute to IP block creators)
            royalty_amount = (chip.price * chip.royalty) / 100
            
            return jsonify({
                "status": "success", 
                "transaction": {
                    "id": transaction.id,
                    "chipId": transaction.chip_id,
                    "chipName": chip.name,
                    "price": transaction.price,
                    "buyer": buyer,
                    "timestamp": transaction.timestamp.isoformat() if transaction.timestamp else datetime.now().isoformat(),
                    "status": transaction.status
                },
                "royalty": {
                    "id": f"royalty_{str(uuid.uuid4())[:12]}",
                    "chipId": chip_id,
                    "designer": chip.designer,
                    "amount": royalty_amount,
                    "timestamp": datetime.now().isoformat()
                }
            })
        finally:
            db.close()
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/marketplace/stats', methods=['GET'])
def get_marketplace_stats():
    """Get marketplace statistics"""
    db = SessionLocal()
    try:
        chips = crud.get_chips(db)
        # In a real implementation, we would also get transactions and royalties from the database
        # For now, we'll simulate this data
        total_revenue = sum(chip.revenue for chip in chips)
        total_transactions = sum(chip.sales for chip in chips)
        total_royalties = sum((chip.price * chip.royalty / 100) * chip.sales for chip in chips)
        
        return jsonify({
            "status": "success",
            "statistics": {
                "totalChips": len(chips),
                "totalTransactions": total_transactions,
                "totalRevenue": total_revenue,
                "totalRoyalties": total_royalties
            }
        })
    finally:
        db.close()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)